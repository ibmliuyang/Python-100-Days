import os
from docx import Document

# 指定输入文件夹和输出文件名
input_folder = "/Users/ly/Documents/产品-项目/1000-税务共享/100-平安银行/1000-交付物/会议纪要"
output_file = os.path.join(input_folder, "all.docx")

# 创建一个新的文档
merged_doc = Document()

# 遍历指定文件夹下的所有Word文档
for filename in os.listdir(input_folder):
    if filename.endswith(".docx"):
        # 打开每个Word文档
        doc = Document(os.path.join(input_folder, filename))

        # 将文档内容复制到合并的文档中
        for element in doc.element.body:
            merged_doc.element.body.append(element)

# 保存合并后的文档
merged_doc.save(output_file)

print(f"合并完成，结果保存在: {output_file}")
