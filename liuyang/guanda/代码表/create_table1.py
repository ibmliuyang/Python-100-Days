import pandas as pd

# 加载Excel文件
xls = pd.ExcelFile('/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/dmb_gd_out3.xlsx')

excel_file_path = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/代码表清单104个.xlsx'

# 读取Excel文件
daimabiaoqingdan = pd.read_excel(excel_file_path)

table_id ="_id varchar(64), \n"
table_yuliuziduan ="taxpayer_no      VARCHAR(30) COMMENT '纳税人识别号', \ntaxpayer         VARCHAR(200) COMMENT '纳税人名称', \ngroup_no         VARCHAR(100) COMMENT '组织编码', \ngroup_name       VARCHAR(200) COMMENT '组织名称', \ncreate_time      DATETIME COMMENT '创建时间', \ncreate_user_id   VARCHAR(64) COMMENT '创建人ID', \ncreate_user_name VARCHAR(50) COMMENT '创建人名称', \nupdate_time      DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间', \nupdate_user_id   VARCHAR(64) COMMENT '更新人ID', \nupdate_user_name VARCHAR(50) COMMENT '更新人名称', \nreserved1        VARCHAR(10) COMMENT '预留字段1', \nreserved2        VARCHAR(10) COMMENT '预留字段2', \nreserved3        VARCHAR(10) COMMENT '预留字段3', \nreserved4        VARCHAR(10) COMMENT '预留字段4', \nreserved5        VARCHAR(10) COMMENT '预留字段5', \nreserved6        VARCHAR(10) COMMENT '预留字段6', \nreserved7        VARCHAR(10) COMMENT '预留字段7', \nreserved8        VARCHAR(10) COMMENT '预留字段8', \nreserved9        VARCHAR(10) COMMENT '预留字段9', \nreserved10       VARCHAR(10) COMMENT '预留字段10', \nPRIMARY KEY (id)"

i = 0
# 打开一个文件用于写入DDL语句
with open('/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/dmb_ddl.sql', 'w') as ddl_file:
    # 对于每个sheet，生成并写入建表语句
    for sheet_name in xls.sheet_names:

        specific_row = daimabiaoqingdan.iloc[i]  # 获取对应行的数据
        table_name = specific_row[2]  # 假设表名在第2列

        table_name_lower = table_name.lower()
        # 提取最后一个下划线后面的内容
        id_prefix = table_name_lower.split('_')[-1]


        i += 1
        # 读取sheet内容
        df = xls.parse(sheet_name)

        # 获取表的注释、字段名、类型、长度、描述
        table_comment = str(df.iloc[0, 0]).strip()
        columns_info = df.iloc[2:, [1, 2, 4, 5, 6]]



        fields_sql = ',\n'.join([
            f'{str(col_name).strip()} {("DECIMAL" if str(col_type).strip().upper() == "NUMBER" else str(col_type).strip())}({str(col_length).strip()}) COMMENT \"{str(desc).strip()}\"'
            for desc, col_name, col_type, col_length, _ in columns_info.itertuples(index=False)
            if pd.notnull(col_name) and pd.notnull(col_type) and pd.notnull(col_length)
        ])

        fields_sql = id_prefix + table_id + fields_sql+","

        # 构建完整的建表SQL语句，包括检查表是否存在并相应处理
        create_table_sql = (
            f"drop table if exists {table_name_lower};\n\n"
            f"create table {table_name_lower} (\n{fields_sql}\n{table_yuliuziduan}\n)  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT '直连申报:{table_comment}';\n\n"
        )

        # 写入到文件
        ddl_file.write(create_table_sql)

print("DDL语句已成功写入到ddl.txt")