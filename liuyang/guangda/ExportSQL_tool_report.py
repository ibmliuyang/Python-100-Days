import pymysql
import re
from pymysql import Error


class SQLExporter:
    def __init__(self, host, user, password, database, port=3306):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.connection = None

    def connect(self):
        """建立数据库连接"""
        try:
            self.connection = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor  # 使用DictCursor方便处理结果
            )
            print(f"已连接到数据库: {self.database} (端口: {self.port})")
            return True
        except Error as e:
            print(f"数据库连接错误: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection and self.connection.open:
            self.connection.close()
            print("已断开数据库连接")

    def execute_query(self, query):
        """
        执行查询并返回结果
        """
        if not self.connection or not self.connection.open:
            if not self.connect():
                return [], []

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)

                # 处理非SELECT语句的情况
                if cursor.description is None:
                    return [], []

                records = cursor.fetchall()
                # 转换为元组列表和列名列表
                if records and isinstance(records[0], dict):
                    columns = list(records[0].keys())
                    records = [tuple(record.values()) for record in records]
                else:
                    columns = [column[0] for column in cursor.description]

                return records, columns
        except Error as e:
            print(f"查询执行错误: {e}")
            return [], []

    def extract_where_clause(self, query):
        """从SELECT查询中提取WHERE子句（不改变原始大小写）"""
        # 去除注释（保持大小写）
        query = re.sub(r"/\*.*?\*/", "", query, flags=re.DOTALL)
        query = re.sub(r"--.*$", "", query, flags=re.M)
        query = query.strip()

        # 使用不区分大小写的正则表达式查找WHERE子句位置
        where_match = re.search(r"\s+WHERE\s+(.+)$", query, re.IGNORECASE | re.DOTALL)
        if where_match:
            where_clause = where_match.group(1)

            # 移除ORDER BY, LIMIT等子句（不区分大小写）
            where_clause = re.sub(r"\s+ORDER\s+BY\s+.*$", "", where_clause, flags=re.IGNORECASE)
            where_clause = re.sub(r"\s+LIMIT\s+.*$", "", where_clause, flags=re.IGNORECASE)
            where_clause = re.sub(r"\s+OFFSET\s+.*$", "", where_clause, flags=re.IGNORECASE)

            return where_clause.strip()

        return None

    def generate_delete_sql(self, query, table_name=None):
        """根据SELECT查询的WHERE条件生成DELETE语句"""
        if not table_name:
            table_name = self._extract_table_name(query)
            if not table_name:
                print(f"错误: 无法从查询中推断表名: {query[:50]}...")
                return ""

        # 提取WHERE子句（不包含WHERE关键字）
        where_conditions = self.extract_where_clause(query)
        if not where_conditions:
            print(f"警告: 无法从查询中提取WHERE条件: {query[:50]}...")
            print("将生成无条件DELETE语句，这可能删除表中所有数据！如需继续，请手动执行。")
            return ""

        # 生成DELETE语句（正确拼接WHERE关键字）
        return f"DELETE FROM {table_name} WHERE {where_conditions};"



    def generate_insert_sql(self, query, table_name=None, batch_size=1000):
        """
        生成多行INSERT SQL语句（批量插入）
        """
        records, columns = self.execute_query(query)
        if not records or not columns:
            print(f"警告: 查询 '{query[:50]}...' 没有返回数据")
            return ""

        if not table_name:
            table_name = self._extract_table_name(query)
            if not table_name:
                print(f"错误: 无法从查询中推断表名: {query[:50]}...")
                return ""

        # 生成列名列表
        columns_str = ", ".join(columns)

        # 分批处理，避免SQL语句过长
        insert_sql = []
        for i in range(0, len(records), batch_size):
            batch_records = records[i:i + batch_size]
            values_groups = []

            for record in batch_records:
                values = []
                for value in record:
                    if value is None:
                        values.append("NULL")
                    elif isinstance(value, (int, float)):
                        values.append(str(value))
                    elif isinstance(value, bool):
                        values.append(str(int(value)))
                    elif isinstance(value, str):
                        escaped = value.replace("'", "''")
                        values.append(f"'{escaped}'")
                    else:
                        values.append(f"'{str(value)}'")

                # 将当前行的值用括号包裹，形成一个值组
                values_groups.append(f"({', '.join(values)})")

            # 合并多行值组到一个INSERT语句
            values_str = ",\n".join(values_groups)
            insert_sql.append(f"INSERT INTO {table_name} ({columns_str}) VALUES\n{values_str};")

        return "\n\n".join(insert_sql)





    def _extract_table_name(self, query):
        """
        改进的表名提取方法（使用正则表达式）
        """
        query = re.sub(r"/\*.*?\*/", "", query, flags=re.DOTALL)  # 去除注释
        query = query.strip().lower()

        # 匹配简单SELECT语句
        from_match = re.search(r"from\s+([\w\.]+)", query)
        if from_match:
            table_name = from_match.group(1)
            return table_name.split(".")[-1]

        # 匹配INSERT/UPDATE/DELETE语句
        for verb in ["insert into", "update", "delete from"]:
            if query.startswith(verb):
                return query.split(verb)[1].split()[0].split(".")[-1]

        return None

    def export_to_file(self, query, output_file, table_name=None, batch_size=1000, include_delete=True):
        """导出SQL到文件（可选包含DELETE语句）"""
        sql_parts = []

        if include_delete:
            delete_sql = self.generate_delete_sql(query, table_name)
            if delete_sql:
                sql_parts.append(delete_sql)

        insert_sql = self.generate_insert_sql(query, table_name, batch_size)
        if insert_sql:
            sql_parts.append(insert_sql)

        combined_sql = "\n\n".join(sql_parts)

        if combined_sql:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(combined_sql)
                print(f"SQL 已导出到文件: {output_file}")
            except Exception as e:
                print(f"导出文件时出错: {e}")

    def process_multiple_queries(self, queries, output_file=None, include_comments=True, batch_size=1000,
                                 include_delete=True):
        """处理多个查询（可选包含DELETE语句）"""
        all_sql = []

        for query in queries:
            query = query.strip()
            if not query:
                continue

            sql_parts = []

            if include_delete:
                delete_sql = self.generate_delete_sql(query)
                if delete_sql:
                    if include_comments:
                        sql_parts.append(f"-- DELETE 语句基于查询条件: {query}\n{delete_sql}")
                    else:
                        sql_parts.append(delete_sql)

            insert_sql = self.generate_insert_sql(query, batch_size=batch_size)
            if insert_sql:
                if include_comments:
                    sql_parts.append(f"-- 原始查询: {query}\n{insert_sql}")
                else:
                    sql_parts.append(insert_sql)

            if sql_parts:
                all_sql.append("\n\n".join(sql_parts))

        combined_sql = "\n\n\n".join(all_sql)

        if output_file and combined_sql:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(combined_sql)
                print(f"所有 SQL 已导出到文件: {output_file}")
            except Exception as e:
                print(f"导出文件时出错: {e}")

        return combined_sql
# 使用示例
if __name__ == "__main__":
    exporter = SQLExporter(
        host="tms-edb-dd.eca.dev.cebbank",
        user="tms_user",
        password="Tms@1234",
        database="tms",
        port=16310
    )
#  去掉 "select *  from t_tool_index where  report_id  in  ('0c8020e2b8054a75a4809f1000000101','0c8020e2b8054a75a4809f1000000102')"
# index 表从everDB复制，从这里导出会丢失/, 比如 \",###.00\" 替换为  \\",###.00\\"
    queries = [
        "select *  from t_tool_report where  report_code in ('10101320','10101319')"
    ]

    exporter.process_multiple_queries(queries, output_file="tool_report_250612.sql")
    exporter.disconnect()