import os
import comtypes.client


def convert_doc_to_docx(input_dir, output_dir):
    # 获取Word应用程序对象
    word = comtypes.client.CreateObject('Word.Application')
    word.Visible = False  # 设置为不可见，以便在后台运行

    # 遍历输入目录中的所有.doc文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.doc'):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename.replace('.doc', '.docx'))

            # 打开.doc文件
            doc = word.Documents.Open(input_path)

            # 保存为.docx文件
            doc.SaveAs(output_path, FileFormat=16)  # 16 for DOCX

            # 关闭文档，不保存更改（因为我们刚刚已经保存了）
            doc.Close(False)

            # 退出Word应用程序
    word.Quit()


# 使用示例
input_directory = '/Users/ly/Downloads/doc2docx'  # 替换为你的.doc文件所在的目录
output_directory = '/Users/ly/Downloads/doc2docx/docx'  # 替换为你想要保存.docx文件的目录
convert_doc_to_docx(input_directory, output_directory)