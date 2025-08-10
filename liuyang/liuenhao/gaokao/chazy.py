import pandas as pd
import re

# 定义文件路径
like_majors_path = "我喜欢的专业.xlsx"
physics_group_path = "2025高考-物理组-排序.xlsx"
result_path = "专业——匹配.xlsx"

# 读取"我喜欢的专业.xlsx"，获取喜欢的专业列表
# 假设"我喜欢的专业"列在表格中的索引为0（第一列）
like_majors_df = pd.read_excel(like_majors_path)
like_majors = [str(major).strip() for major in like_majors_df.iloc[:, 0].dropna()]
# 去除重复的专业关键词
like_majors = list(set(like_majors))
# 按关键词长度降序排序，避免短关键词先匹配（如"计算机"和"计算"）
like_majors.sort(key=lambda x: len(x), reverse=True)

# 读取"2025高考-物理组-排序.xlsx"数据
# 假设"专业名称"列在表格中的索引为4（第五列）
physics_group_df = pd.read_excel(physics_group_path, sheet_name='Sheet1')


# 定义专业名称清洗函数，去除括号及其中的内容
def clean_major_name(name):
    cleaned = re.sub(r'[（\(\[【].*?[）\)\]】]', '', str(name))
    return cleaned.strip()


# 存储匹配结果
result_data = []

# 遍历高考物理组数据
for index, row in physics_group_df.iterrows():
    # 获取原始专业名称
    original_major = str(row.iloc[4])  # 假设专业名称在第5列（索引4）
    # 清洗专业名称
    cleaned_major = clean_major_name(original_major)

    # 检查是否匹配喜欢的专业
    matched_major = None
    for major in like_majors:
        # 如果清洗后的专业名称包含喜欢的专业关键词
        if major in cleaned_major:
            matched_major = major
            break  # 找到最长匹配后退出循环

    if matched_major:
        result_data.append({
            '序号': row.iloc[0],  # 假设序号在第1列（索引0）
            '院校名称': row.iloc[2],  # 假设院校名称在第3列（索引2）
            '匹配的专业关键词': matched_major,
            '原始专业名称': original_major,
            '清洗后专业名称': cleaned_major,
            '投档最低分': row.iloc[5]  # 假设投档分在第6列（索引5）
        })

# 保存结果到Excel
result_df = pd.DataFrame(result_data)
result_df.to_excel(result_path, index=False, sheet_name='专业匹配结果')

print(f"匹配完成，共找到 {len(result_data)} 条匹配记录，已保存至 {result_path}")
