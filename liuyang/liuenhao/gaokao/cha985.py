import pandas as pd
import re

# 文件路径
file_path_1 = "2025高考-物理组-排序.xlsx"
file_path_2 = "985院校.xlsx"
result_path = "985院校——1匹配.xlsx"

# 读取Excel文件
df1 = pd.read_excel(file_path_1, sheet_name='Sheet1')
df2 = pd.read_excel(file_path_2, sheet_name='Sheet1')

# 提取985院校列表（B列，索引1）并去重，同时按长度降序排序（避免短名称先匹配）
df2_schools = [str(school).strip() for school in df2.iloc[:, 1].dropna()]
df2_schools = list(set(df2_schools))  # 去重
df2_schools.sort(key=lambda x: len(x), reverse=True)  # 长名称优先匹配


# 定义处理院校名称的函数：去除所有括号及其中的内容，同时移除"独立学院"关键词
def clean_school_name(name):
    # 正则表达式匹配所有全角/半角括号及其中的内容（包括()[]【】）
    cleaned = re.sub(r'[（\(\[【].*?[）\)\]】]', '', str(name))
    # 彻底移除"独立学院"关键词（无论是否在括号中）
    cleaned = cleaned.replace('独立学院', '')
    # 去除可能的空格
    return cleaned.strip()


# 存储匹配结果
result_data = []

# 遍历高考分数线数据
for index, row in df1.iterrows():
    # 获取原始院校名称并清洗
    original_name = row.iloc[2]  # C列（索引2）
    # 新增判断：如果原始名称包含"独立学院"，直接跳过本条记录

    if "独立学院" in original_name:
        continue  # 跳过当前循环，进入下一行数据处理

    cleaned_name = clean_school_name(original_name)

    # 检查是否有985院校名称是当前学校名称的前缀，且清洗后名称不包含"独立学院"
    matched_school = None
    for school in df2_schools:
        # 双重条件：前缀匹配 + 不包含独立学院关键词
        if cleaned_name.startswith(school) and '独立学院' not in cleaned_name:
            matched_school = school
            break  # 找到最长匹配后退出循环

    if matched_school:
        result_data.append({
            '序号': row.iloc[0],  # A列（索引0）
            '匹配的985院校': matched_school,  # 匹配上的985院校名称
            '原始学校名称': original_name,  # 原始名称用于核对
            '清洗后名称': cleaned_name,  # 清洗后的名称
            '专业': row.iloc[4],  # E列（索引4）
            '投档最低分': row.iloc[5]  # F列（索引5）
        })

# 保存结果
result_df = pd.DataFrame(result_data)
result_df.to_excel(result_path, index=False, sheet_name='匹配结果')

print(f"匹配完成，共找到 {len(result_data)} 条匹配记录，已保存至 {result_path}")
