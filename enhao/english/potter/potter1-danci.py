import re
from collections import Counter
import csv
import nltk
import ssl

# 禁用SSL验证
ssl._create_default_https_context = ssl._create_unverified_context
# 下载停用词资源
nltk.download('stopwords')

from nltk.corpus import stopwords


def extract_and_count_english_words(srt_path, csv_path, custom_exclude_words=None):
    with open(srt_path, 'r', encoding='utf-8') as srt_file:
        srt_content = srt_file.read()

    # 使用正则表达式提取英文单词
    english_words = re.findall(r'\b[A-Za-z]+\b', srt_content)

    # 使用NLTK库获取英语停用词列表
    stop_words = set(stopwords.words('english'))

    # 添加自定义排除的单词
    if custom_exclude_words:
        stop_words.update(custom_exclude_words)

    # 移除停用词
    english_words = [word for word in english_words if word.lower() not in stop_words]

    # 使用Counter进行单词计数
    word_counts = Counter(english_words)

    # 按重复次数从多到少降序排列
    sorted_word_counts = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)

    with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
        # 创建CSV写入对象
        csv_writer = csv.writer(csv_file)

        # 写入CSV文件头部
        csv_writer.writerow(['Word', 'Count'])

        # 将提取到的英文单词及其重复次数按降序写入CSV文件
        for word, count in sorted_word_counts:
            csv_writer.writerow([word, count])


# 输入SRT文件路径和输出CSV文件路径
srt_path = '/Users/ly/Downloads/哈利1-魔法石/ha-1.srt'
csv_path = '/Users/ly/Downloads/哈利1-魔法石/ha-danci-5.csv'

# 指定要排除的单词
custom_exclude_words = set(
    ['you', 'I', 's', 'the', 'to', 'a', 't', 'it', 'of', 'that', 'is', 'and', 'You', 'Harry', 'in', 'be', 'on', 'me',
     'It', 'your', 'he', 'this', 're', 'not', 'What', 'are', 'for', 'do', 'what', 'know', 'have', 'there', 'was', 'm',
     'don', 'one', 'with', 'up', 'Potter', 'He', 'll', 've', 'The', 'But', 'see', 'That', 'all', 'we', 'And', 'my',
     'will', 'We', 'him', 'can', 'about', 'No', 'like', 'got', 'go', 'at', 'going', 'right', 'here', 'as', 'get', 'if',
     'There', 'no', 'his', 'now', 'A', 'out', 'who', 'from', 'Now', 'This', 'Not', 'Well', 'but', 'they', 'Good', 'so',
     'were', 'come', 'then', 'd', 'Oh', 'day', 'only', 'How', 'how', 'just', 'off', 'Who', 'an', 'back', 'again',
     'really', 'has', 'name', 'never', 'more', 'first', 'way', 'good', 'boy', 'Do', 'Theywant', 'had', 'well', 'Go'])

# 调用函数提取英文单词并计数，并按降序排列写入CSV文件
extract_and_count_english_words(srt_path, csv_path, custom_exclude_words)
