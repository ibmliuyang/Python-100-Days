import openpyxl

file_path ="/Users/ly/Downloads/2021-yanfajiaji-fuzhu1.xlsx"

# 读取Excel文件
wb = openpyxl.load_workbook(file_path)

# 遍历所有sheet页
for sheet in wb:
    print(f"Sheet: {sheet.title}")
    for row in sheet.iter_rows(values_only=True):
        if isinstance(row[5], (int, float)):
            print(row[5])