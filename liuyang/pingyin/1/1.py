import os
import pandas as pd
from pypinyin import pinyin, Style

# 指定目录
directory = "/Users/ly/Downloads/手工税种-建表excel"

# 获取目录下所有的Excel文件
excel_files = [file for file in os.listdir(directory) if file.endswith(".xlsx") and "~" not in file]

for file in excel_files:
    # 读取原始Excel文件
    original_excel = pd.read_excel(os.path.join(directory, file), header=None)

    # 提取第一列数据
    first_column = original_excel.iloc[:, 0]

    # 将中文转换为拼音首字母
    pinyin_first_letter = ["".join(p[0] for p in pinyin(str(item), style=Style.FIRST_LETTER)) if isinstance(item, str) else item for item in first_column]

    # 创建新的DataFrame
    new_excel = pd.DataFrame({'原文件名': first_column, '拼音首字母': pinyin_first_letter})

    # 创建新文件名
    new_filename = file.split(".xlsx")[0] + "_pinyin.xlsx"

    # 保存新Excel文件
    new_excel.to_excel(os.path.join(directory, new_filename), index=False, engine='openpyxl')
