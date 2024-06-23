import os
from docx import Document

# 设置源目录和目标文件路径
source_dir = '/Users/ly/Downloads/liuyang_bak'
target_file = '/Users/ly/Downloads/liuyang_bak/kaoshi.txt'

# 确保目标文件是空的或不存在，以便我们可以从头开始写入
with open(target_file, 'w', encoding='utf-8') as f:
    f.write('')

# 遍历源目录下的所有文件
for filename in os.listdir(source_dir):
    if filename.endswith('.docx'):
        # 构造完整的文件路径
        file_path = os.path.join(source_dir, filename)

        # 打开Word文档并读取内容
        doc = Document(file_path)

        # 这里我们简单地将所有段落的文本写入到目标文件中
        # 你可以根据需要修改这部分代码来提取特定的信息或进行其他处理
        with open(target_file, 'a', encoding='utf-8') as f:
            for para in doc.paragraphs:
                f.write(para.text + '\n')
            f.write('\n' + '-' * 50 + '\n\n')  # 添加分隔线以便区分不同的文档

print(f"处理完成，结果已写入到 {target_file}")