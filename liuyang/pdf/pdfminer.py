from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager,PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
#rb以二进制读模式打开本地pdf文件
fp = open('pdf/0.pdf','rb')
#创建一个pdf文档分析器
parser = PDFParser(fp)
#创建一个PDF文档
doc=PDFDocument(parser)
#创建PDf资源管理器
resource = PDFResourceManager()
#创建一个PDF参数分析器
laparams = LAParams()

