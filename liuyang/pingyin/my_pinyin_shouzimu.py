from xpinyin import Pinyin

def get_first_letter(text):
    p = Pinyin()
    initials = p.get_initials(text, '')
    return initials.lower()  # 将拼音首字母转换为小写

# 示例
text = "账务归属分行一级分行"
result = get_first_letter(text)
print(result)
