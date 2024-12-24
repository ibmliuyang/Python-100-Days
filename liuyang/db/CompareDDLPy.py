import pymysql
import pandas as pd
from configparser import ConfigParser
import argparse

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.expand_frame_repr', False)


# 根据数据库名称读取对应的配置文件
def read_db_config(db_name):
    config_filename = f'{db_name}_db_config.ini'
    parser = ConfigParser()
    parser.read(config_filename)

    if parser.has_section('database'):
        items = parser.items('database')
        config = {k: v for k, v in items}
        config['port'] = int(config.get('port', 3306))
        return config
    else:
        raise Exception(f'database section not found in the {config_filename} file')


def get_table_columns(db_name):
    db_config = read_db_config(db_name)

    conn = pymysql.connect(
        host=db_config.get('host', 'localhost'),
        user=db_config.get('user', 'root'),
        password=db_config.get('password', ''),
        database=db_name,
        port=db_config['port'],
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
            return df
    finally:
        conn.close()


def compare_databases(old_db_name, new_db_name):
    old_df = get_table_columns(old_db_name)
    new_df = get_table_columns(new_db_name)

    new_df['source'] = new_db_name
    old_df['source'] = old_db_name

    # 找出新数据库中存在但旧数据库中不存在的表
    new_tables = new_df[~new_df['TABLE_NAME'].isin(old_df['TABLE_NAME'])]
    new_table_ddl = []
    for _, row in new_tables.iterrows():
        table_name = row['TABLE_NAME']
        columns = []
        for index, value in row.iteritems():
            if index in ['TABLE_NAME','source']:
                continue
            column_name = value['COLUMN_NAME']
            data_type = value['DATA_TYPE']
            is_nullable = value['IS_NULLABLE']
            char_max_length = value['CHARACTER_MAXIMUM_LENGTH']
            if char_max_length:
                data_type += f'({char_max_length})'
            columns.append(f'{column_name} {data_type} {is_nullable}')
        columns_sql = ', '.join(columns)
        new_table_ddl.append(f'CREATE TABLE {table_name} ({columns_sql});')

    # 找出新、旧数据库都存在但结构有差异的表
    common_tables = new_df[new_df['TABLE_NAME'].isin(old_df['TABLE_NAME'])]
    common_table_ddl = []
    for table_name in common_tables['TABLE_NAME'].unique():
        new_table_cols = new_df[new_df['TABLE_NAME'] == table_name]
        old_table_cols = old_df[old_df['TABLE_NAME'] == table_name]

        for _, new_col in new_table_cols.iterrows():
            column_name = new_col['COLUMN_NAME']
            data_type = new_col['DATA_TYPE']
            is_nullable = new_col['IS_NULLABLE']
            char_max_length = new_col['CHARACTER_MAXIMUM_LENGTH']
            if char_max_length:
                data_type = data_type.split('(')[0]  # 提取基本数据类型

            old_col = old_table_cols[old_table_cols['COLUMN_NAME'] == column_name]
            if old_col.empty:
                common_table_ddl.append(f'ALTER TABLE {table_name} ADD COLUMN {column_name} {data_type} {is_nullable};')
            else:
                old_type = old_col['DATA_TYPE'].values[0].split('(')[0]  # 提取基本数据类型
                old_nullable = old_col['IS_NULLABLE'].values[0]  # 定义old_nullable
                if (old_type!= data_type or old_nullable!= is_nullable) or (
                        char_max_length is not None and old_col['CHARACTER_MAXIMUM_LENGTH'].values[0]!= char_max_length):
                    common_table_ddl.append(f'ALTER TABLE {table_name} MODIFY COLUMN {column_name} {data_type} {is_nullable};')

    return new_table_ddl + common_table_ddl


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate DDL SQL based on database differences")
    parser.add_argument("old_db", help="The old database name")
    parser.add_argument("new_db", help="The new database name")

    args = parser.parse_args()

    ddl_sqls = compare_databases(args.old_db, args.new_db)
    for ddl_sql in ddl_sqls:
        print(ddl_sql)
