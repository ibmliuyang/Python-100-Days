import pandas as pd
import re


def split_excel_to_sheets(input_file, output_file):
    # 读取Excel文件
    df = pd.read_excel(input_file)


    # 初始化一个ExcelWriter对象，用于写入多个sheet
    writer = pd.ExcelWriter(output_file, engine='openpyxl')

    # 初始化变量来跟踪当前sheet的索引和数据
    current_sheet_index = 0
    sheet_data = []
    sheet_names = []

    first_sheet = "1.电子类表证单书种类代码表"
    # 遍历DataFrame的每一行
    for i, row in df.iterrows():
        # 使用正则表达式匹配以数字+点+汉字开始的行
        match = re.match(r'^\d+\.\s*\w+', str(row[0]))
        # 收集当前行的数据到sheet_data

        if match:
            print(str(row[0]))
            # 如果找到匹配，则先保存之前的数据到sheet（如果存在）
            if sheet_data:
                sheet_names.append(f'{first_sheet}')
                sheet_df = pd.DataFrame(sheet_data)
                sheet_df.to_excel(writer, sheet_name=f'{first_sheet}', index=False)
                sheet_data = []  # 重置sheet_data以便收集下一个sheet的数据
                first_sheet = str(row[0])
        sheet_data.append(row.tolist())


    # 处理最后一个sheet的数据（循环结束后剩余的数据）
    if sheet_data:
        sheet_df = pd.DataFrame(sheet_data)
        sheet_df.to_excel(writer, sheet_name=f'{first_sheet}', index=False)
        sheet_names.append(f'{first_sheet}')

    # 保存到新的Excel文件
    writer.save()

    print(f"已成功拆分为{len(sheet_names)}个sheet：{', '.join(sheet_names)}")


# 使用函数，输入和输出文件请按实际情况替换
input_path = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/dmb_gd.xlsx'
output_path = '/Users/ly/ynworkspace/Python-100-Days/liuyang/guanda/代码表/dmb_gd_out3.xlsx'
split_excel_to_sheets(input_path, output_path)
