import os
import pandas as pd
from pypinyin import pinyin, Style
import re  # 导入正则表达式模块

# 指定目录路径
#directory = '/Users/ly/Downloads/手工税种-建表excel/new/'
directory = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/createtable/pingyin/pab_table/gd'

# 获取目录中的所有Excel文件
excel_files = [f for f in os.listdir(directory) if f.endswith('.xlsx') and "~" not in f]

# 公共字段定义
common_fields = [
    "`ssqj` varchar(20)  CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '所属期间',",
    "`group_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '机构代码',",
    "`group_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '机构名称',",
    "`taxpayer_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '纳税人识别号',",
    "`taxpayer` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '纳税人名称',",
    "`is_valid` tinyint NULL DEFAULT NULL COMMENT '是否有效 0:无效,1:有效[dict:is_valid]',",
    "`enable_status` tinyint NULL DEFAULT NULL COMMENT '启用状态 0:未启用1:已启用[dict:enable_status]',",
    "`create_user_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '创建人ID',",
    "`create_user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '创建人名称',",
    "`create_time` datetime NULL DEFAULT NULL COMMENT '创建时间',",
    "`update_user_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '更新人ID',",
    "`update_user_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '更新人名称',",
    "`update_time` datetime NULL DEFAULT NULL COMMENT '更新时间',",
    "`tenant_code` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '租户编码',",
    "`reserved1` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段1',",
    "`reserved2` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段2',",
    "`reserved3` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段3',",
    "`reserved4` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段4',",
    "`reserved5` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段5',",
    "`reserved6` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段6',",
    "`reserved7` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段7',",
    "`reserved8` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段8',",
    "`reserved9` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段9',",
    "`reserved10` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NULL DEFAULT NULL COMMENT '预留字段10',"
]

# 处理每个Excel文件
for excel_file in excel_files:
    # 读取Excel文件
    file_path = os.path.join(directory, excel_file)
    df = pd.read_excel(file_path, header=None)

    # 获取表名（Excel第一行第一列）
    id_name = ''.join([''.join(i[0]) for i in pinyin(df.iloc[0, 0], style=Style.FIRST_LETTER, strict=False)])
    table_name = 't_zzs_'+id_name
    table_comment = df.iloc[0, 0]  # 使用Excel中的内容作为表的COMMENT

    # 获取列名和字段类型
    columns = df.iloc[1:, 0].apply(lambda x: ''.join([''.join(re.findall(r'[0-9a-zA-Z\u4e00-\u9fa5_]+', i[0])) for i in pinyin(x, style=Style.FIRST_LETTER, strict=False)])[:50])



    column_comments = df.iloc[1:, 0]  # 使用Excel中的内容作为字段的COMMENT
    data_types = df.iloc[1:, 1]
    varchar_lengths = df.iloc[1:, 2]  # 第三列的数据用于指定VARCHAR长度

    # 生成SQL文件的文件名
    sql_file_path = os.path.join(directory, table_name + '.sql')

    # 生成DDL语句
    ddl_statements = []
    ddl_statements.append(f"CREATE TABLE {table_name} (")

    # 添加主键
    ddl_statements.append(f"`{id_name}_id` BIGINT UNSIGNED AUTO_INCREMENT COMMENT '主键',")

    for col, col_comment, data_type, varchar_length in zip(columns, column_comments, data_types, varchar_lengths):
        # 将汉字数据类型转换为MySQL数据类型
        if data_type == "字符串":
            # 如果第三列有值，使用它来指定VARCHAR长度，否则默认为64
            varchar_length = int(varchar_length) if pd.notna(varchar_length) else 64
            mysql_data_type = f"varchar({varchar_length}) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        elif data_type == "金额":
            mysql_data_type = "decimal(20, 2)"
        elif data_type == "日期":
            mysql_data_type = "datetime"
        else:
            mysql_data_type = "VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"

        ddl_statements.append(f"`{col}` {mysql_data_type} COMMENT '{col_comment}',")

    # 添加公共字段
    ddl_statements.extend(common_fields)

    # 移除最后一个逗号，并添加结束括号
    ddl_statements[-1] = ddl_statements[-1][:-1]
    ddl_statements.append(f", PRIMARY KEY (`{id_name}_id`)")

    ddl_statements.append(f") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT '{table_comment}';")

    # 写入SQL文件
    with open(sql_file_path, 'w') as sql_file:
        for statement in ddl_statements:
            sql_file.write(statement + '\n')

print("SQL文件生成完成。")

