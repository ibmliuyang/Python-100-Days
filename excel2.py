import openpyxl

# 打开 Excel 文件
workbook = openpyxl.load_workbook('/Users/ly/Downloads/2021-yanfajiaji-fuzhu1.xlsx')



# 选择第一个 sheet 页
sheet = workbook.worksheets

# 读取第 10 行第 AH 列的内容
cell_value = sheet.cell(row=10, column=6).value

print(cell_value)