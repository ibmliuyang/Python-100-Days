from xpinyin import Pinyin

def get_first_letter(text):
    p = Pinyin()
    pinyin = p.get_pinyin(text, tone_marks='marks', splitter=' ')
    return pinyin

# 示例
text = "账务归属分行一级分行"
result = get_first_letter(text)
print(result)
