import pymysql
import pandas as pd
from configparser import ConfigParser
import argparse

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示完整的列内容
pd.set_option('display.expand_frame_repr', False)  # 禁止换行

# 根据数据库名称读取对应的配置文件
def read_db_config(db_name):
    """Read database configuration file based on db_name and return a dictionary of settings."""
    config_filename = f'{db_name}_db_config.ini'
    parser = ConfigParser()
    parser.read(config_filename)

    if parser.has_section('database'):
        items = parser.items('database')
        return {k: v for k, v in items}
    else:
        raise Exception(f'database section not found in the {config_filename} file')

def get_table_columns(db_name):
    """获取指定数据库的所有表及其字段信息，包括字段长度"""
    db_config = read_db_config(db_name)

    conn = pymysql.connect(
        host=db_config.get('host', 'localhost'),
        user=db_config.get('user', 'root'),
        password=db_config.get('password', ''),
        database=db_name,
        charset='utf8mb4'
    )

    try:
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s;
            """
            cursor.execute(query, (db_name,))
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            if not df.empty:
                print("Column names:", df.columns.tolist())  # 打印列名用于调试
                print("Data types:", df.dtypes)  # 打印各列的数据类型用于调试
            return df
    finally:
        conn.close()

def compare_databases(db1_name, db2_name):
    """比较两个数据库的表结构，包括字段长度"""
    df1 = get_table_columns(db1_name)
    df2 = get_table_columns(db2_name)

    df1['source'] = db1_name
    df2['source'] = db2_name

    diff = pd.concat([df1, df2]).drop_duplicates(
        subset=['TABLE_NAME', 'COLUMN_NAME', 'DATA_TYPE', 'IS_NULLABLE', 'CHARACTER_MAXIMUM_LENGTH'],
        keep=False
    )

    return diff

if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Compare two MySQL databases.")
    parser.add_argument("db1", help="The first database name to compare")
    parser.add_argument("db2", help="The second database name to compare")

    args = parser.parse_args()

    # 比较两个数据库
    differences = compare_databases(args.db1, args.db2)

    if not differences.empty:
        print("Differences found:")
        print(differences)
    else:
        print("No differences found.")