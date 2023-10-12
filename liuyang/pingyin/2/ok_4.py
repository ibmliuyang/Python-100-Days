import os
import pandas as pd
from pypinyin import pinyin, Style

# 指定目录路径
directory = '/Users/ly/Downloads/手工税种-建表excel/new/'

# 获取目录中的所有Excel文件
excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')  and "~" not in f]

# 处理每个Excel文件
for excel_file in excel_files:
    # 读取Excel文件
    file_path = os.path.join(directory, excel_file)
    df = pd.read_excel(file_path, header=None)

    # 获取表名（Excel第一行第一列）
    id_name = ''.join([''.join(i[0]) for i in pinyin(df.iloc[0, 0], style=Style.FIRST_LETTER, strict=False)])

    table_name = 't_sgsz_' + id_name

    table_comment = df.iloc[0, 0]  # 使用Excel中的内容作为表的COMMENT

    # 获取列名和字段类型
    columns = df.iloc[1:, 0].apply(lambda x: ''.join([''.join(i[0]) for i in pinyin(x, style=Style.FIRST_LETTER, strict=False)]))
    column_comments = df.iloc[1:, 0]  # 使用Excel中的内容作为字段的COMMENT
    data_types = df.iloc[1:, 1]

    # 生成SQL文件的文件名
    # sql_file_name = os.path.splitext(excel_file)[0] + '.sql'
    sql_file_path = os.path.join(directory, table_name+'.sql')

    # 生成DDL语句
    ddl_statements = []
    ddl_statements.append(f"CREATE TABLE {table_name} (")

    # 添加主键
    ddl_statements.append(f"{id_name}_id BIGINT UNSIGNED AUTO_INCREMENT COMMENT '主键',")

    for col, col_comment, data_type in zip(columns, column_comments, data_types):
        # 将汉字数据类型转换为MySQL数据类型
        if data_type == "字符串":
            mysql_data_type = "VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        elif data_type == "金额":
            mysql_data_type = "DECIMAL(10, 2)"
        elif data_type == "日期":
            mysql_data_type = "DATE"
        else:
            mysql_data_type = "VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"

        ddl_statements.append(f"{col} {mysql_data_type} COMMENT '{col_comment}',")

    # 移除最后一个逗号，并添加结束括号
    ddl_statements[-1] = ddl_statements[-1][:-1]
    ddl_statements.append(f", PRIMARY KEY ({id_name}_id)")

    ddl_statements.append(f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT '{table_comment}';")

    # 写入SQL文件
    with open(sql_file_path, 'w') as sql_file:
        for statement in ddl_statements:
            sql_file.write(statement + '\n')

print("SQL文件生成完成。")
