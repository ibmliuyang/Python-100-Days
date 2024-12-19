import PyPDF2

def extract_all_attachments(pdf_path):
    with open(pdf_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        if hasattr(pdf, '_attachments'):
            for key in pdf._attachments.keys():
                attachment = pdf._attachments[key]
                with open(key, 'wb') as attachment_file:
                    attachment_file.write(attachment)

if __name__ == "__main__":
    pdf_path = "/Users/ly/Downloads/24119221152000162851.pdf"  # 修改为你实际的PDF文件路径，可以是绝对路径或者相对路径（相对当前脚本所在目录）
    extract_all_attachments(pdf_path)