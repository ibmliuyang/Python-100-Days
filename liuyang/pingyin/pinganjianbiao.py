import pandas as pd
from pypinyin import pinyin, Style

# 读取Excel文件
excel_file = "/Users/ly/Downloads/手工税种-建表excel/new/111.xlsx"  # 请将文件名替换为你的Excel文件名
df = pd.read_excel(excel_file, header=None)

# 获取表名（Excel第一行第一列）
table_name = ''.join([''.join(i) for i in pinyin(df.iloc[0, 0], style=Style.FIRST_LETTER, strict=False)])

table_name = 't_sgsz_'+table_name;
# 获取列名和字段类型
columns = df.iloc[1:, 0].apply(lambda x: ''.join([''.join(i[0]) for i in pinyin(x, style=Style.FIRST_LETTER, strict=False)]))
data_types = df.iloc[1:, 1]

# 生成DDL语句
ddl_statements = []
ddl_statements.append(f"CREATE TABLE {table_name} (")

for col, data_type in zip(columns, data_types):
    # 将汉字数据类型转换为MySQL数据类型
    if data_type == "字符串":
        mysql_data_type = "VARCHAR(255)"  # 你可以根据需要修改长度
    elif data_type == "金额":
        mysql_data_type = "DECIMAL(10, 2)"  # 你可以根据需要修改精度和范围
    elif data_type == "日期":
        mysql_data_type = "DATE"
    else:
        mysql_data_type = "VARCHAR(255)"  # 默认为字符串类型

    ddl_statements.append(f"{col} {mysql_data_type},")

# 移除最后一个逗号，并添加结束括号
ddl_statements[-1] = ddl_statements[-1][:-1]
ddl_statements.append(");")

# 打印DDL语句
for statement in ddl_statements:
    print(statement)
