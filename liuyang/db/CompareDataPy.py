import pymysql
import pandas as pd
from configparser import ConfigParser
import argparse

# 设置pandas显示选项
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)  # 自动调整列宽
pd.set_option('display.max_colwidth', None)  # 显示完整的列内容
pd.set_option('display.expand_frame_repr', False)  # 禁止换行


# 根据数据库名称读取对应的配置文件
def read_db_config(db_name, section='database'):
    """Read database configuration file based on db_name and return a dictionary of settings."""
    config_filename = f'{db_name}_db_config.ini'
    parser = ConfigParser()
    parser.read(config_filename)

    if parser.has_section(section):
        items = parser.items(section)
        return {k: v for k, v in items}
    else:
        raise Exception(f'{section} not found in the {config_filename} file')


def get_tables_to_compare(db_name, section='tables_to_compare'):
    """Read table names to compare from the configuration file specific to db_name."""
    config_filename = f'{db_name}_db_config.ini'
    parser = ConfigParser()
    parser.read(config_filename)

    if parser.has_section(section):
        tables = [v for k, v in parser.items(section)]
        return tables
    else:
        raise Exception(f'{section} not found in the {config_filename} file')


def get_table_data(db_name, table_name, source_name=None):
    """获取指定数据库和表的所有数据，并添加来源标识"""
    db_config = read_db_config(db_name)

    conn = pymysql.connect(
        host=db_config.get('host', 'localhost'),
        user=db_config.get('user', 'root'),
        password=db_config.get('password', ''),
        database=db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor  # 使用字典游标
    )
    cursor = conn.cursor()

    query = f"SELECT * FROM `{table_name}`;"

    try:
        cursor.execute(query)
        result = cursor.fetchall()
    except pymysql.Error as err:
        print(f"Error: {err}")
        result = []

    cursor.close()
    conn.close()

    df = pd.DataFrame(result)
    if not df.empty:
        # 将所有列转换为字符串，避免数据类型不一致的问题
        df = df.astype(str)
        # 去除字符串中的空白字符并统一大小写
        df = df.apply(lambda x: x.str.strip().str.lower() if x.dtype == "object" else x)
        # 添加来源标识
        df['source'] = source_name

    return df


def compare_table_data(df1, df2, key_columns=None):
    """比较两个DataFrame的数据，默认使用所有列为key，除非指定了key_columns"""
    if key_columns is None or len(key_columns) == 0:
        raise ValueError("At least one key column must be specified.")

    # 确保两个DataFrame包含相同的列
    common_columns = list(set(df1.columns) & set(df2.columns))
    df1_filtered = df1[common_columns].copy()
    df2_filtered = df2[common_columns].copy()

    # 合并两个DataFrame，并标注来源
    merged_df = pd.merge(df1_filtered, df2_filtered, on=key_columns, how='outer', indicator=True,
                         suffixes=('_df1', '_df2'))

    # 找出仅存在于一个DataFrame中的记录
    only_in_df1 = merged_df[merged_df['_merge'] == 'left_only']
    only_in_df2 = merged_df[merged_df['_merge'] == 'right_only']

    # 对于存在的记录，找出具体哪些字段不同
    both_dfs = merged_df[merged_df['_merge'] == 'both']
    differences = pd.DataFrame()

    for col in common_columns:
        if col not in key_columns:
            diff_rows = both_dfs[both_dfs[f'{col}_df1'] != both_dfs[f'{col}_df2']]
            if not diff_rows.empty:
                diff_rows = diff_rows.rename(columns={f'{col}_df1': col, f'{col}_df2': f'{col}_other'})
                differences = pd.concat([differences, diff_rows], ignore_index=True)

    # 将仅存在于一个DataFrame中的记录和有差异的记录合并
    differences = pd.concat([only_in_df1, only_in_df2, differences], ignore_index=True)

    # 清理合并后的DataFrame，移除多余的来源列
    differences = differences.drop(columns=[c for c in differences.columns if c.endswith('_df1') or c.endswith('_df2')])

    # 如果存在来源标识，确保它们被正确保留
    if 'source_df1' in differences.columns and 'source_df2' in differences.columns:
        differences['source'] = differences.apply(
            lambda row: row['source_df1'] if pd.notnull(row['source_df1']) else row['source_df2'],
            axis=1
        )
        differences = differences.drop(columns=['source_df1', 'source_df2'])

    return differences


if __name__ == "__main__":
    # 设置命令行参数解析
    parser = argparse.ArgumentParser(description="Compare two MySQL databases.")
    parser.add_argument("db1", help="The first database name to compare")
    parser.add_argument("db2", help="The second database name to compare")

    args = parser.parse_args()

    # 获取需要比较的表名
    tables_to_compare_db1 = get_tables_to_compare(args.db1)
    tables_to_compare_db2 = get_tables_to_compare(args.db2)

    # 确保两个数据库中需要比较的表是一致的
    if set(tables_to_compare_db1) != set(tables_to_compare_db2):
        print("Warning: Tables to compare are not the same between the two databases.")
        tables_to_compare = list(set(tables_to_compare_db1).intersection(tables_to_compare_db2))
        if not tables_to_compare:
            print("No common tables to compare. Exiting.")
            exit(1)
    else:
        tables_to_compare = tables_to_compare_db1

    all_differences = []

    for table_name in tables_to_compare:
        print(f"Comparing table: {table_name}")

        df1 = get_table_data(args.db1, table_name, source_name=args.db1)
        df2 = get_table_data(args.db2, table_name, source_name=args.db2)

        if df1.empty or df2.empty:
            print(f"One of the tables '{table_name}' is empty.")
            continue

        # 检查是否存在主键或唯一标识符作为关键字段
        key_columns = ['id'] if 'id' in df1.columns and 'id' in df2.columns else None

        # 比较两个表的数据
        differences = compare_table_data(df1, df2, key_columns=key_columns)

        if not differences.empty:
            differences['表名'] = table_name
            all_differences.append(differences)

    if all_differences:
        all_diffs_df = pd.concat(all_differences, ignore_index=True)
        print("Differences found across multiple tables:")
        print(all_diffs_df[['表名', 'source'] + [col for col in all_diffs_df.columns if
                                                       col not in ['表名', 'source', '_merge']]])
    else:
        print("No differences found across all specified tables.")