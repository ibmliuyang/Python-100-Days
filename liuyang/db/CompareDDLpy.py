import pymysql
import pandas as pd
from configparser import ConfigParser

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示完整的列内容
pd.set_option('display.expand_frame_repr', False)  # 禁止换行

# 读取本地配置文件
def read_db_config(filename='db_config.ini', section='database'):
    """Read database configuration file and return a dictionary of settings."""
    parser = ConfigParser()
    parser.read(filename)

    if parser.has_section(section):
        items = parser.items(section)
        return {k: v for k, v in items}
    else:
        raise Exception(f'{section} not found in the {filename} file')

# 数据库连接配置
db_config = read_db_config()


def get_table_columns(db_name):
    """获取指定数据库的所有表及其字段信息，包括字段长度"""
    # 使用pymysql建立连接
    conn = pymysql.connect(
        host=db_config.get('host', 'localhost'),
        user=db_config.get('user', 'root'),
        password=db_config.get('password', ''),
        database=db_config.get('database', ''),
        charset='utf8mb4'  # 可根据实际需求设置字符集
    )
    print(conn)
    try:
        with conn.cursor() as cursor:
            query = """
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s;
            """
            cursor.execute(query, (db_name,))
            result = cursor.fetchall()
            # 将查询结果转换为DataFrame
            df = pd.DataFrame(result)
            # 打印列名，用于调试，查看是否与期望一致
            print("Column names:", df.columns)
            # 打印各列的数据类型，用于调试，查看是否存在类型不一致情况
            print("Data types:", df.dtypes)
            return df
    finally:
        conn.close()


def compare_databases(db1_name, db2_name):
    """比较两个数据库的表结构，包括字段长度"""
    df1 = get_table_columns(db1_name)
    df2 = get_table_columns(db2_name)

    # 添加来源标识
    df1['source'] = db1_name
    df2['source'] = db2_name

    # 合并两个DataFrame以找出不同之处，现在也考虑字段长度
    diff = pd.concat([df1, df2]).drop_duplicates(
        subset=['TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE', 'IS_NULLABLE', 'CHARACTER_MAXIMUM_LENGTH'],
        keep=False
    )

    return diff


if __name__ == "__main__":
    # 比较两个数据库
    differences = compare_databases('a', 'aa')

    if not differences.empty:
        print("Differences found:")
        print(differences)
    else:
        print("No differences found.")