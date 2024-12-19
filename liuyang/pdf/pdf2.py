from pdfminer.high_level import extract_text

def extract_text_from_pdf(pdf_path):
    text = extract_text(pdf_path)
    print(text)

if __name__ == "__main__":
    pdf_path = "/Users/ly/Downloads/24119221152000162851.pdf"  # 修改为你实际的PDF文件路径，可以是绝对路径或者相对路径（相对当前脚本所在目录）
    extract_text_from_pdf(pdf_path)