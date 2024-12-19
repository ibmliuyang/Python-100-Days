import os

# 定义目录路径
directory = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/createtable/pingyin/pab_table/gd'

# 列出目录下的所有.sql文件
sql_files = [f for f in os.listdir(directory) if f.endswith(".sql")]

# 生成drop语句
drop_statements = [f"DROP TABLE IF EXISTS {file_name[:-4]};" for file_name in sql_files]

# 合并所有.sql文件内容到一个文件
with open(os.path.join(directory, "all_careta_table.sql"), "w") as output_file:
    # 写入生成的drop语句
    output_file.write("\n".join(drop_statements) + "\n\n")

    # 逐个读取.sql文件并写入到合并文件中
    for sql_file in sql_files:
        with open(os.path.join(directory, sql_file), "r") as input_file:
            output_file.write(input_file.read() + "\n\n")

print("合并完成，并生成了drop语句。")
