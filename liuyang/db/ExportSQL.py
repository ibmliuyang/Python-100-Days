import mysql.connector
import re
from mysql.connector import Error


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
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            if self.connection.is_connected():
                print(f"已连接到数据库: {self.database} (端口: {self.port})")
                return True
        except Error as e:
            print(f"数据库连接错误: {e}")
            return False

    def disconnect(self):
        """断开数据库连接"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("已断开数据库连接")

    def execute_query(self, query):
        """
        执行查询并返回结果
        """
        if not self.connection or not self.connection.is_connected():
            if not self.connect():
                return [], []

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)

            # 处理非SELECT语句的情况
            if not cursor.with_rows:
                cursor.close()
                return [], []

            records = cursor.fetchall()
            columns = [column[0] for column in cursor.description]
            cursor.close()
            return records, columns
        except Error as e:
            print(f"查询执行错误: {e}")
            return [], []

    def generate_insert_sql(self, query, table_name=None):
        """
        生成 INSERT SQL 语句
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

        insert_sql = []
        for record in records:
            values = []
            for value in record:
                if value is None:
                    values.append("NULL")
                elif isinstance(value, (int, float)):
                    values.append(str(value))
                elif isinstance(value, bool):
                    values.append(str(int(value)))  # 或使用'TRUE'/'FALSE'
                elif isinstance(value, str):
                    escaped = value.replace("'", "''")
                    values.append(f"'{escaped}'")
                else:
                    values.append(f"'{str(value)}'")

            columns_str = ", ".join(columns)
            values_str = ", ".join(values)
            insert_sql.append(
                f"INSERT INTO {table_name} ({columns_str}) VALUES ({values_str});"
            )

        return "\n".join(insert_sql)

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

    def export_to_file(self, query, output_file, table_name=None):
        insert_sql = self.generate_insert_sql(query, table_name)
        if insert_sql:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(insert_sql)
                print(f"INSERT SQL 已导出到文件: {output_file}")
            except Exception as e:
                print(f"导出文件时出错: {e}")

    def process_multiple_queries(self, queries, output_file=None, include_comments=True):
        all_insert_sql = []
        for query in queries:
            query = query.strip()
            if not query:
                continue

            insert_sql = self.generate_insert_sql(query)
            if not insert_sql:
                continue

            if include_comments:
                header = f"-- 原始查询: {query}\n" if len(query) < 75 else f"-- 原始查询: {query[:75]}...\n"
                all_insert_sql.append(header + insert_sql)
            else:
                all_insert_sql.append(insert_sql)

        combined_sql = "\n\n".join(all_insert_sql)

        if output_file and combined_sql:
            try:
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(combined_sql)
                print(f"所有 INSERT SQL 已导出到文件: {output_file}")
            except Exception as e:
                print(f"导出文件时出错: {e}")

        return combined_sql


# 使用示例
if __name__ == "__main__":
    exporter = SQLExporter(
        host="192.168.12.100",
        user="taxmpv5dev",
        password="5VtAxmP@M362",
        database="taxmpv5db_dev",
        port=33305
    )

    queries = [
        "select *  from t_tool_report where   report_id in ('1400159778100019200', '1397996648607580160');",
        "select *  from t_tool_report_tpl  where   report_id in ('1400159778100019200', '1397996648607580160')",
        "select *  from t_tool_report_config where   report_id in ('1400159778100019200', '1397996648607580160');",
    ]

    exporter.process_multiple_queries(queries, output_file="batch_inserts.sql")
    exporter.disconnect()
