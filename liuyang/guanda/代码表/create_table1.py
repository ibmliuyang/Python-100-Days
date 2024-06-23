import pandas as pd

# 加载Excel文件
xls = pd.ExcelFile('/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/dmb_gd_out3.xlsx')

excel_file_path = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/代码表清单104个.xlsx'

# 读取Excel文件
daimabiaoqingdan = pd.read_excel(excel_file_path)

i = 0
# 对于每个sheet，生成并打印建表语句
for sheet_name in xls.sheet_names:
    i += 1
    specific_row = daimabiaoqingdan.iloc[i]  # 获取第100行（索引为99）
    # print(specific_row)
    table_name = specific_row[2]
    # 读取sheet


    df = xls.parse(sheet_name)

    # 获取表名、字段名、类型、长度、描述
    table_comment = str(df.iloc[0, 0]).strip()  # 确保表名为字符串并去除空白
    columns_info = df.iloc[2:, [1, 2, 4, 5, 6]]  # 分别对应C4, E4, F4, D4, G4列
    # 1    电子表证单书种类代码 dzbzdszlDm N VARCHAR 10

    # 构建字段定义部分的SQL字符串，确保长度和类型为字符串
    fields_sql = ',\n'.join([
        f'`{str(col_name).strip()}` {str(col_type).strip()}({str(col_length).strip()}) COMMENT \"{str(_).strip()}\"'
        for _, col_name, col_type, col_length, col_desc in columns_info.itertuples(index=False)
        if pd.notnull(col_name) and pd.notnull(col_type) and pd.notnull(col_length)
    ])

    # 完整的建表SQL语句
    create_table_sql = f"CREATE TABLE `{table_name}` (\n{fields_sql}\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci  COMMENT {table_comment};"
    print(create_table_sql)
    print("\n---\n")  # 分隔符，方便区分每个表的建表语句