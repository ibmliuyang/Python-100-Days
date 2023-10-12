import os
import pandas as pd
from xpinyin import Pinyin

# 设置目录路径
directory_path = "/Users/ly/Downloads/手工税种-建表excel"

# 初始化拼音转换器
p = Pinyin()

# 遍历指定目录中的Excel文件
for filename in os.listdir(directory_path):
    if filename.endswith(".xlsx"):  # 只处理Excel文件
        file_path = os.path.join(directory_path, filename)

        # 读取Excel文件并手动指定引擎
        df = pd.read_excel(file_path, engine='openpyxl')

        # 复制第一列到第二列
        df['拼音'] = df.iloc[:, 0]

        # 将第一列中文的拼音首字母放入第二列
        def get_first_letter(text):
            initials = p.get_initials(text, '')
            return initials.lower()  # 将拼音首字母转换为小写

        df['拼音'] = df['拼音'].apply(get_first_letter)

        # 创建新的Excel文件名
        new_filename = os.path.splitext(filename)[0] + "_pinyin.xlsx"
        new_file_path = os.path.join(directory_path, new_filename)

        # 保存修改后的Excel文件
        df.to_excel(new_file_path, index=False)

        print(f"已处理文件: {filename}")

print("所有文件处理完成")
