import pandas as pd

# 假设你的Excel文件名为'input.xlsx'，并且你想从名为'Sheet1'的sheet开始
file_name = '/Users/ly/Downloads/dmb_gd.xlsx'
sheet_name = 'Sheet1'
output_file_name =  '/Users/ly/Downloads/dmb_gd_out2.xlsx'

# 读取Excel文件
df = pd.read_excel(file_name, sheet_name=sheet_name)

# 初始化一个空的字典来存储拆分后的数据
split_dfs = {}
current_sheet_name = None
current_df = pd.DataFrame()

# 遍历DataFrame的行
for index, row in df.iterrows():
    # 检查行是否以"1."、"2."等开头的字符串
    for i in range(1, 105):  # 1到104
        if str(row.iloc[0]).startswith(f"{i}."):  # 假设我们要检查的列是第一列
            # 如果当前DataFrame不为空，则将其写入之前的sheet，并重置
            if not current_df.empty:
                split_dfs[current_sheet_name] = current_df
                current_df = pd.DataFrame()
                # 设置新的sheet名称
            current_sheet_name = f'Sheet_{i}'
            break  # 跳出内层循环
    # 将当前行添加到当前的DataFrame中
    current_df = current_df.append(row, ignore_index=True)

# 处理最后一个sheet（如果有的话）
if not current_df.empty:
    split_dfs[current_sheet_name] = current_df

# 写入新的Excel文件
with pd.ExcelWriter(output_file_name, engine='openpyxl') as writer:
    for sheet_name, df in split_dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)

print(f'Excel文件已拆分成{len(split_dfs)}个sheet并保存到{output_file_name}')