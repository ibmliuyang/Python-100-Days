import pymysql


def get_table_ddl(connection, table_name):
    try:
        with connection.cursor() as cursor:
            # 查询表的 DDL 语句
            cursor.execute(f"SHOW CREATE TABLE {table_name}")
            result = cursor.fetchone()
            if result:
                return result[1]
            return None
    except Exception as e:
        print(f"获取表 {table_name} 的 DDL 语句时出错: {e}")
        return None


def generate_ddl_and_drop_statements(host, port , user, password, database, table_names):
    try:
        # 建立数据库连接
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )

        all_statements = []
        for table_name in table_names:
            drop_statement = f"DROP TABLE IF EXISTS {table_name};"
            all_statements.append(drop_statement)
            ddl = get_table_ddl(connection, table_name)
            if ddl:
                all_statements.append(ddl + ";")

        # 打印生成的语句
        for statement in all_statements:
            print(statement)

    except pymysql.Error as e:
        print(f"数据库连接出错: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

if __name__ == "__main__":
    # 数据库连接信息
    host = '192.168.12.100'
    port = 33305
    user = 'taxmpv6dev'
    password = 'v6_TaXp@dM'
    database = 'taxmpv6db_dev'
    # 表名列表
    table_names = ['t_sys_menu', 'iv_iinv_invoice', 'iv_iinv_email']

    generate_ddl_and_drop_statements(host, port, user, password, database, table_names)