import re

strings = ["1.电子类表证单书种类代码表", "2.单书种", "3.哈哈哈"]
cleaned_strings = []

for s in strings:
    cleaned_string = re.sub(r'^\d+\.', '', s)  # 使用正则表达式去掉数字和点
    cleaned_strings.append(cleaned_string)

print(cleaned_strings)