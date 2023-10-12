import pandas as pd

# 读取excel文件
file = '/Users/ly/Downloads/2021-yanfajiaji-fuzhu1.xlsx'



# 读取excel文件
xl = pd.read_excel(file, sheet_name=None)

# 获取sheet页名称的列表
sheet_names = xl.keys()

# 打印sheet页的数量
print(f"Number of sheets: {len(sheet_names)}")

# 打印sheet页名称列表
print(f"Sheet names: {sheet_names}")
