import pandas as pd
import json

# 读取Excel文件
#excel_file = '测试生成报文.xlsx'  # 替换为你的Excel文件路径
excel_file = '算税过程表.xlsx'  # 替换为你的Excel文件路径
df = pd.read_excel(excel_file, skiprows=1)

# 删除所有未命名的列
df = df.fillna('')

# 将DataFrame转换为JSON
json_data = df.to_dict(orient='records')

# 打印JSON数据
print(json.dumps(json_data, indent=2))

# 如果需要保存到文件
with open('output.json', 'w') as f:
    json.dump(json_data, f, indent=2)