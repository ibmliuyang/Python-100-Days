import re
import langid
from translate import Translator
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

def translate_to_chinese(sentence):
    # 使用 langid 进行语言检测
    lang, _ = langid.classify(sentence)
    print(sentence)
    # 如果检测到的语言是英文，进行中文翻译
    if lang == 'en':
        translator = Translator(to_lang='zh')
        chinese_sentence = translator.translate(sentence)
        print(chinese_sentence)
        return chinese_sentence
    else:
        return sentence

def translate_and_write_to_txt(english_sentences, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        for sentence in english_sentences:
            translation = translate_to_chinese(sentence)
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
