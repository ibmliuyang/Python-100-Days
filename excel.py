import pandas as pd

filename = "/Users/ly/Downloads/2021-yanfajiaji-fuzhu.xls"  # 请替换为您的excel文件名

# 读取excel文件
xl = pd.read_excel(filename, sheet_name=None)

# 遍历所有sheet页，提取第AH列第10行的内容
for sheet_name, df in xl.items():
    value = df.at[9:1]  # 注意：索引从0开始，所以第10行对应索引为9
    print(f"Sheet {sheet_name}: {value}")