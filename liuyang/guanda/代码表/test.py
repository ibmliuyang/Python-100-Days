import pandas as pd

# Excel文件路径
excel_file_path = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/代码表清单104个.xlsx'

# 读取Excel文件
df = pd.read_excel(excel_file_path)

# 遍历数据框的每一行并打印指定的列
for index, row in df.iterrows():
    # 打印序号、表名和对应的代码表
    print(f"{row[0]}	{row[1]}	{row[2]}")