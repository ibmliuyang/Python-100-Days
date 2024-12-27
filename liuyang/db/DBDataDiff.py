import pymysql
import pandas as pd
from configparser import ConfigParser
import argparse


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


def read_tables_to_compare(db_name):
    config_filename = f'{db_name}_db_config.ini'
    parser = ConfigParser()
    parser.read(config_filename)

    if parser.has_section('tables_to_compare'):
        return parser.get('tables_to_compare', 'tables').split(',')
    else:
        raise Exception(f'tables_to_compare section not found in the {config_filename} file')


def get_table_data(db_name, table_name):
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
        query = f"SELECT * FROM {table_name}"
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            df = pd.DataFrame(result)
            return df
    finally:
        conn.close()


def get_primary_key(db_name, table_name):
    db_config = read_db_config(db_name)
    conn = pymysql.connect(
        host=db_config.get('host', 'localhost'),
        user=db_config.get('user', 'root'),
        password=db_config.get('password', ''),
        database='information_schema',
        port=db_config['port'],
        charset='utf8mb4'
    )

    try:
        query = f"""
            SELECT COLUMN_NAME
            FROM KEY_COLUMN_USAGE
            WHERE TABLE_SCHEMA = '{db_name}'
            AND TABLE_NAME = '{table_name}'
            AND CONSTRAINT_NAME = 'PRIMARY'
        """
        with conn.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                raise Exception(f"Primary key not found for table {table_name} in database {db_name}")
    finally:
        conn.close()


def compare_tables(old_db_name, new_db_name, table_name):
    old_df = get_table_data(old_db_name, table_name)
    new_df = get_table_data(new_db_name, table_name)

    insert_sqls = []
    replace_sqls = []

    id_column = get_primary_key(old_db_name, table_name)
    if id_column not in old_df.columns or id_column not in new_df.columns:
        raise Exception(f"Table {table_name} does not have the expected primary key column {id_column}")

    old_ids = set(old_df[id_column])
    new_ids = set(new_df[id_column])

    for _, new_row in new_df.iterrows():
        new_id = new_row[id_column]
        if new_id not in old_ids:
            columns = ', '.join(new_df.columns)
            values = ', '.join([f'"{value}"' if isinstance(value, str) else str(value) for value in new_row])
            insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            insert_sqls.append(insert_sql)
        else:
            old_row = old_df[old_df[id_column] == new_id]
            # 检查除id外其他字段是否相同
            other_columns = [col for col in new_df.columns if col!= id_column]
            if not old_row[other_columns].equals(new_df[other_columns].loc[new_row.name]):
                columns = ', '.join(new_df.columns)
                values = ', '.join([f'"{value}"' if isinstance(value, str) else str(value) for value in new_row])
                replace_sql = f"REPLACE INTO {table_name} ({columns}) VALUES ({values})"
                replace_sqls.append(replace_sql)

    return insert_sqls, replace_sqls


def generate_sqls(old_db_name, new_db_name):
    tables_to_compare = read_tables_to_compare(old_db_name)
    all_insert_sqls = []
    all_replace_sqls = []

    for table in tables_to_compare:
        insert_sqls, replace_sqls = compare_tables(old_db_name, new_db_name, table)
        all_insert_sqls.extend(insert_sqls)
        all_replace_sqls.extend(replace_sqls)

    return all_insert_sqls, all_replace_sqls


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate INSERT/REPLACE SQL based on database differences")
    parser.add_argument("old_db", help="The old database name")
    parser.add_argument("new_db", help="The new database name")

    args = parser.parse_args()

    insert_sqls, replace_sqls = generate_sqls(args.old_db, args.new_db)

    print("Insert SQLs:")
    for sql in insert_sqls:
        print(sql)

    print("\nReplace SQLs:")
    for sql in replace_sqls:
        print(sql)