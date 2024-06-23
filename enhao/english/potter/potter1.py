import re
from googletrans import Translator
import pyperclip

def extract_english_sentences_from_srt(srt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 使用正则表达式提取英文句子
    pattern = re.compile(r'\d+\n([\s\S]*?)\n\n', re.MULTILINE)
    matches = pattern.findall(content)

    # 清理空格和换行符
    english_sentences = [re.sub(r'\s+', ' ', sentence.strip()) for sentence in matches]

    return english_sentences

def translate_to_chinese_with_retry(sentence, translator, max_retries=3):
    for _ in range(max_retries):
        try:
            translation = translator.translate(sentence, dest='zh-cn').text
            return translation
        except Exception as e:
            print(f"翻译失败，正在重试... 错误信息: {e}")
    raise Exception("翻译失败，已达到最大重试次数")

def translate_and_write_to_txt(english_sentences, output_file_path):
    translator = Translator()

    with open(output_file_path, 'w', encoding='utf-8') as file:
        for sentence in english_sentences:
            translation = translate_to_chinese_with_retry(sentence, translator)
            file.write(translation + '\n')

if __name__ == "__main__":
    # 输入和输出文件路径
    src_file_path = "/Users/ly/Downloads/哈利1-魔法石/ha-1.srt"
    output_file_path = "/Users/ly/Downloads/哈利1-魔法石/ha-1.txt"

    # 提取英文句子
    english_sentences = extract_english_sentences_from_srt(src_file_path)

    # 逐行翻译并写入到txt文件
    translate_and_write_to_txt(english_sentences, output_file_path)

    print("翻译完成，结果已保存到", output_file_path)
