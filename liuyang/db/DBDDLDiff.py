# 导入 pymysql 库，用于连接和操作 MySQL 数据库
import pymysql
# 导入 pandas 库，用于数据处理和分析，它提供了高效的数据结构和数据操作方法
import pandas as pd
# 导入 ConfigParser 类，用于读取配置文件，方便管理数据库连接等配置信息
from configparser import ConfigParser
# 导入 argparse 库，用于处理命令行参数，使程序可以通过命令行接收输入
import argparse

# 设置 pandas 的显示选项，让 DataFrame 显示时展示所有列
pd.set_option('display.max_columns', None)
# 设置 pandas 的显示选项，自动调整显示宽度以适应内容
pd.set_option('display.width', None)
# 设置 pandas 的显示选项，让列内容完整显示，不截断
pd.set_option('display.max_colwidth', None)
# 设置 pandas 的显示选项，禁止将数据框换行显示，以紧凑形式展示
pd.set_option('display.expand_frame_repr', False)


# 定义函数 read_db_config，功能是根据传入的数据库名称读取对应的配置文件
def read_db_config(db_name):
    # 生成配置文件名，格式为 {数据库名}_db_config.ini
    config_filename = f'{db_name}_db_config.ini'
    # 创建 ConfigParser 对象，用于解析配置文件
    parser = ConfigParser()
    # 读取配置文件
    parser.read(config_filename)
    # 检查配置文件中是否存在 'database' 这个节
    if parser.has_section('database'):
        # 获取 'database' 节中的所有键值对
        items = parser.items('database')
        # 将键值对转换为字典形式，方便后续使用
        config = {k: v for k, v in items}
        # 将配置中的端口号转换为整数类型，如果没有指定端口号，则使用默认值 3306
        config['port'] = int(config.get('port', 3306))
        # 返回包含数据库连接配置信息的字典
        return config
    else:
        # 如果配置文件中没有 'database' 节，抛出异常并提示在哪个文件中未找到
        raise Exception(f'database section not found in the {config_filename} file')


# 定义函数 get_table_columns，功能是获取指定数据库中所有表的列信息
def get_table_columns(db_name):
    # 调用 read_db_config 函数，读取指定数据库的配置信息
    db_config = read_db_config(db_name)
    # 使用 pymysql 连接到 MySQL 数据库，传入数据库连接所需的各项配置信息
    conn = pymysql.connect(
        # 数据库主机地址，如果配置中没有指定，则使用默认值 'localhost'
        host=db_config.get('host', 'localhost'),
        # 数据库用户名，如果配置中没有指定，则使用默认值 'root'
        user=db_config.get('user', 'root'),
        # 数据库密码，如果配置中没有指定，则使用默认值空字符串
        password=db_config.get('password', ''),
        # 要连接的数据库名称
        database=db_name,
        # 数据库端口号，从配置中获取
        port=db_config['port'],
        # 数据库连接使用的字符集，设置为 'utf8mb4'
        charset='utf8mb4'
    )
    try:
        # 使用 with 语句创建游标对象，并且指定游标以字典形式返回查询结果
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 定义 SQL 查询语句，从 information_schema.COLUMNS 表中获取指定数据库中所有表的列信息
            query = """
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE, IS_NULLABLE, CHARACTER_MAXIMUM_LENGTH, COLUMN_COMMENT
            FROM information_schema.COLUMNS
            WHERE TABLE_SCHEMA = %s;
            """
            # 执行 SQL 查询语句，传入数据库名称作为参数
            cursor.execute(query, (db_name,))
            # 获取所有查询结果
            result = cursor.fetchall()
            # 将查询结果转换为 pandas 的 DataFrame 格式，方便后续处理和分析
            df = pd.DataFrame(result)
            # 返回包含所有表列信息的 DataFrame
            return df
    finally:
        # 无论 try 块中的代码是否执行成功，最终都要关闭数据库连接，释放资源
        conn.close()


# 定义函数 get_create_table_ddl，功能是获取指定数据库中指定表的创建 DDL 语句
def get_create_table_ddl(db_name, table_name):
    # 调用 read_db_config 函数，读取指定数据库的配置信息
    db_config = read_db_config(db_name)
    # 使用 pymysql 连接到 MySQL 数据库，传入数据库连接所需的各项配置信息
    conn = pymysql.connect(
        # 数据库主机地址，如果配置中没有指定，则使用默认值 'localhost'
        host=db_config.get('host', 'localhost'),
        # 数据库用户名，如果配置中没有指定，则使用默认值 'root'
        user=db_config.get('user', 'root'),
        # 数据库密码，如果配置中没有指定，则使用默认值空字符串
        password=db_config.get('password', ''),
        # 要连接的数据库名称
        database=db_name,
        # 数据库端口号，从配置中获取
        port=db_config['port'],
        # 数据库连接使用的字符集，设置为 'utf8mb4'
        charset='utf8mb4'
    )
    try:
        # 使用 with 语句创建游标对象
        with conn.cursor() as cursor:
            # 定义 SQL 查询语句，获取指定表的创建语句
            query = f"SHOW CREATE TABLE {table_name}"
            # 执行 SQL 查询语句
            cursor.execute(query)
            # 获取查询结果，这里查询结果是一个包含表创建语句的元组
            result = cursor.fetchone()
            # 如果查询结果不为空，说明获取到了表的创建语句
            if result:
                # 返回表创建语句，元组中的第二个元素就是创建表的 DDL 语句
                return result[1]
            else:
                # 如果没有获取到表的创建语句，返回 None
                return None
    finally:
        # 无论 try 块中的代码是否执行成功，最终都要关闭数据库连接，释放资源
        conn.close()


# 定义函数 compare_databases，功能是比较两个数据库的结构差异并生成相应的 DDL 语句
def compare_databases(old_db_name, new_db_name):
    # 调用 get_table_columns 函数，获取旧数据库中所有表的列信息
    old_df = get_table_columns(old_db_name)
    # 调用 get_table_columns 函数，获取新数据库中所有表的列信息
    new_df = get_table_columns(new_db_name)
    # 为新数据库的 DataFrame 添加一个名为'source' 的列，值为新数据库名称
    new_df['source'] = new_db_name
    # 为旧数据库的 DataFrame 添加一个名为'source' 的列，值为旧数据库名称
    old_df['source'] = old_db_name
    # 初始化一个空列表，用于存储生成的 DDL 语句
    ddl_sqls = []

    # 找出新数据库中存在但旧数据库中不存在的表
    new_tables = new_df[~new_df['TABLE_NAME'].isin(old_df['TABLE_NAME'])]
    # 遍历新数据库中新增的表名
    for table_name in new_tables['TABLE_NAME'].unique():
        # 获取新增表的创建 DDL 语句
        create_table_ddl = get_create_table_ddl(new_db_name, table_name)
        # 如果获取到了创建 DDL 语句
        if create_table_ddl:
            # 将创建 DDL 语句添加到 ddl_sqls 列表中
            ddl_sqls.append(create_table_ddl)
        else:
            # 如果没有获取到创建 DDL 语句，说明需要手动生成
            table_columns = new_tables[new_tables['TABLE_NAME'] == table_name]
            # 初始化一个空列表，用于存储列定义
            column_defs = []
            # 遍历新增表的每一列
            for _, row in table_columns.iterrows():
                # 获取列名
                column_name = row['COLUMN_NAME']
                # 获取数据类型
                data_type = row['DATA_TYPE']
                # 获取是否可为空的信息
                is_nullable = row['IS_NULLABLE']
                # 获取字符最大长度信息
                char_max_length = row['CHARACTER_MAXIMUM_LENGTH']
                # 获取列注释信息，如果存在的话
                column_comment = row['COLUMN_COMMENT'] if 'COLUMN_COMMENT' in row else ''

                # 如果数据类型是以 'int' 开头，即整数类型
                if data_type.startswith('int'):
                    # 根据是否可为空设置 nullable_str
                    nullable_str = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                    # 生成列定义字符串
                    column_def = f'{column_name} {data_type} {nullable_str}'
                else:
                    # 如果数据类型是以 'varchar' 开头且字符最大长度不为空
                    if data_type.startswith('varchar') and pd.notnull(char_max_length):
                        # 格式化数据类型，带上字符最大长度
                        data_type = f'varchar({int(char_max_length)})'
                    # 根据是否可为空设置 nullable_str
                    nullable_str = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                    # 生成列定义字符串
                    column_def = f'{column_name} {data_type} {nullable_str}'

                # 如果有列注释
                if column_comment:
                    # 在列定义字符串中添加注释
                    column_def += f" COMMENT '{column_comment}'"
                # 将生成的列定义添加到 column_defs 列表中
                column_defs.append(column_def)
            # 将所有列定义用逗号连接成一个字符串
            columns_sql = ', '.join(column_defs)
            # 生成创建表的 DDL 语句并添加到 ddl_sqls 列表中
            ddl_sqls.append(f'CREATE TABLE {table_name} ({columns_sql});')

    # 找出新、旧数据库中都存在的表
    common_tables = new_df[new_df['TABLE_NAME'].isin(old_df['TABLE_NAME'])]
    # 遍历这些共同存在的表名
    for table_name in common_tables['TABLE_NAME'].unique():
        # 获取新数据库中该表的列信息
        new_table_cols = new_df[new_df['TABLE_NAME'] == table_name]
        # 获取旧数据库中该表的列信息
        old_table_cols = old_df[old_df['TABLE_NAME'] == table_name]

        # 遍历新数据库中该表的每一列
        for _, new_col in new_table_cols.iterrows():
            # 获取列名
            column_name = new_col['COLUMN_NAME']
            # 获取数据类型
            data_type = new_col['DATA_TYPE']
            # 获取是否可为空的信息
            is_nullable = new_col['IS_NULLABLE']
            # 获取字符最大长度信息
            char_max_length = new_col['CHARACTER_MAXIMUM_LENGTH']
            # 获取列注释信息，如果存在的话
            column_comment = new_col['COLUMN_COMMENT'] if 'COLUMN_COMMENT' in new_col else ''

            # 如果数据类型是以 'int' 开头，即整数类型
            if data_type.startswith('int'):
                # 根据是否可为空设置 nullable_str
                nullable_str = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                # 生成列定义字符串
                column_def = f'{column_name} {data_type} {nullable_str}'
            else:
                # 如果数据类型是以 'varchar' 开头且字符最大长度不为空
                if data_type.startswith('varchar') and pd.notnull(char_max_length):
                    # 格式化数据类型，带上字符最大长度
                    data_type = f'varchar({int(char_max_length)})'
                # 根据是否可为空设置 nullable_str
                nullable_str = 'NULL' if is_nullable == 'YES' else 'NOT NULL'
                # 生成列定义字符串
                column_def = f'{column_name} {data_type} {nullable_str}'

            # 如果有列注释
            if column_comment:
                # 在列定义字符串中添加注释
                column_def += f" COMMENT '{column_comment}'"

            # 在旧数据库的该表列信息中查找同名列
            old_col = old_table_cols[old_table_cols['COLUMN_NAME'] == column_name]
            # 如果旧数据库中不存在该列
            if old_col.empty:
                # 生成添加列的 DDL 语句并添加到 ddl_sqls 列表中
                ddl_sqls.append(f'ALTER TABLE {table_name} ADD COLUMN {column_def};')
            else:
                # 获取旧数据库中该列的数据类型
                old_type = old_col['DATA_TYPE'].values[0]
                # 如果旧数据类型是以 'varchar' 开头且没有括号且字符最大长度不为空
                if old_type.startswith('varchar') and '(' not in old_type and pd.notnull(char_max_length):
                    # 格式化旧数据类型，带上字符最大长度
                    old_type = f'varchar({int(char_max_length)})'
                # 获取旧数据库中该列是否可为空的信息
                old_nullable = old_col['IS_NULLABLE'].values[0]
                # 根据旧数据库中该列是否可为空设置 old_nullable_str
                old_nullable_str = 'NULL' if old_nullable == 'YES' else 'NOT NULL'
                # 如果旧数据类型、是否可为空或字符最大长度与新列不同
                if (old_type!= data_type or old_nullable_str!= nullable_str) or (
                        pd.notnull(char_max_length) and old_col['CHARACTER_MAXIMUM_LENGTH'].values[0]!= char_max_length):
                    # 生成修改列的 DDL 语句并添加到 ddl_sqls 列表中
                    ddl_sqls.append(f'ALTER TABLE {table_name} MODIFY COLUMN {column_def};')

    # 返回生成的所有 DDL 语句列表
    return ddl_sqls


if __name__ == "__main__":
    # 创建一个命令行参数解析器对象，用于解析命令行输入的参数
    parser = argparse.ArgumentParser(description="Generate DDL SQL based on database differences")
    # 添加一个位置参数 'old_db'，用于接收旧数据库名称，并提供参数说明
    parser.add_argument("old_db", help="The old database name")
    # 添加一个位置参数 'new_db'，用于接收新数据库名称，并提供参数说明
    parser.add_argument("new_db", help="The new database name")

    # 解析命令行输入的参数
    args = parser.parse_args()
    # 调用 compare_databases 函数，比较旧数据库和新数据库的结构差异，并生成 DDL 语句
    ddl_sqls = compare_databases(args.old_db, args.new_db)
    # 遍历生成的 DDL 语句列表
    for ddl_sql in ddl_sqls:
        # 打印每条 DDL 语句
        print(ddl_sql)