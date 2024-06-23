import pandas as pd

# 读取Excel文件
excel_file = '/Users/ly/Documents/产品-项目/105-时代电气/架构评审/总体架构/数据结构-字段.xlsx'
df = pd.read_excel(excel_file)

# 合并"表名"列相同内容的数据
df['表名'] = df.groupby('表名')['表名'].transform(lambda x: ', '.join(x.drop_duplicates()))

# 保存修改后的Excel文件
output_file = '/Users/ly/Documents/产品-项目/105-时代电气/架构评审/总体架构/数据结构-字段-合并.xlsx'
df.to_excel(output_file, index=False)

