import pandas as pd
from pypinyin import pinyin, Style

# 读取Excel文件
excel_file = "/Users/ly/Downloads/手工税种-建表excel/new/111.xlsx"  # 请将文件名替换为你的Excel文件名
df = pd.read_excel(excel_file, header=None)

# 获取表名（Excel第一行第一列）
table_name = ''.join([''.join(i[0]) for i in pinyin(df.iloc[0, 0], style=Style.FIRST_LETTER, strict=False)])
table_comment = df.iloc[0, 0]  # 使用Excel中的内容作为表的COMMENT

# 获取列名和字段类型
columns = df.iloc[1:, 0].apply(lambda x: ''.join([''.join(i[0]) for i in pinyin(x, style=Style.FIRST_LETTER, strict=False)]))
column_comments = df.iloc[1:, 0]  # 使用Excel中的内容作为字段的COMMENT
data_types = df.iloc[1:, 1]

# 生成DDL语句
ddl_statements = []
ddl_statements.append(f"CREATE TABLE {table_name} (")

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
ddl_statements.append(f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT '{table_comment}';")

# 打印DDL语句
for statement in ddl_statements:
    print(statement)
