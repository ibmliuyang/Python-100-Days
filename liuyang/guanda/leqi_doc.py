import pandas as pd
from openpyxl import Workbook

# 读取Excel文件
file_path = '/Users/ly/Downloads/dmb_gd.xlsx'  # 修改为正确的文件路径
try:
    df = pd.read_excel(file_path, sheet_name='Sheet1')  # 假设数据在Sheet1中
except ValueError:
    print(f"Worksheet named 'Sheet1' not found in {file_path}. Please check the sheet name and file path.")
    exit(1)

# 初始化一个字典，用于存储拆分后的数据
sheet_dict = {}

# 根据拆分规则进行拆分
current_sheet = None
for index, row in df.iterrows():
    if pd.notna(row[0]) and str(row[0]).endswith('.'):
        try:
            sheet_number = int(row[0][:-1])  # 去除最后的"."并转换为整数
            if 1 <= sheet_number <= 104:
                current_sheet = f'Sheet_{sheet_number}'
                sheet_dict[current_sheet] = pd.DataFrame(columns=df.columns)  # 创建新的DataFrame
        except ValueError:
            pass
    if current_sheet:
        sheet_dict[current_sheet] = sheet_dict[current_sheet].append(row, ignore_index=True)

# 将拆分后的数据写入新的Excel文件
output_file = '/Users/ly/Downloads/dmb_gd_out.xlsx'  # 修改为输出文件路径

# 创建一个新的空工作簿
wb = Workbook()

# 再次使用pd.ExcelWriter写入数据，使用engine_kwargs传递额外的引擎参数
with pd.ExcelWriter(output_file, engine='openpyxl', engine_kwargs={'workbook': wb}) as writer:
    for sheet_name, sheet_data in sheet_dict.items():
        # 检查工作表是否有数据，只有有数据的工作表才写入到 Excel 文件中
        if not sheet_data.empty:
            sheet_data.to_excel(writer, sheet_name=sheet_name, index=False)

# 保存工作簿到文件
wb.save(output_file)
wb.close()

print(f"Excel file successfully split into {len(sheet_dict)} sheets.")
