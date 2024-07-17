import re

from liuyang.guanda.sm4.sm4utils import SM4Util


def process_file(input_filename, output_filename):
    # 正则表达式模式，用于匹配-d后面的内容直到下一个单引号
    pattern = r'-d \'(.*?)\''

    with open(input_filename, 'r') as infile, open(output_filename, 'w') as outfile:
        for line in infile:
            match = re.search(pattern, line)
            if match:
                # 提取匹配的内容
                data = match.group(1)


                encrypted_text = SM4Util.dec(data)
                print(encrypted_text)


                # 将原始行替换为修改后的内容
                line = re.sub(pattern, f'-d \'{encrypted_text}\'', line)
            # 写入新的行到输出文件
            outfile.write(line)


# 调用函数，传入输入和输出文件名
input_filename = 'ssnl.sh'
output_filename = 'ssnl_yuan_req.sh'
process_file(input_filename, output_filename)