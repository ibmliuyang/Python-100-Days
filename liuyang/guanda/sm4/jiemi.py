import re
import os


def read_dmb_file(file_path):
    # 读取文件并找到所有 '-d' 后面的 base64 字符串
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        matches = re.findall(r'-d\s+\'(.*?)\'', content)
    return matches


def decrypt_sm4(key, ciphertexts):
    # 假设 sm4_decrypt 是 sm4util.py 中定义的一个函数
    from sm4util import sm4_decrypt

    decrypted_texts = []
    for ciphertext in ciphertexts:
        decrypted_text = sm4_decrypt(key, ciphertext)
        decrypted_texts.append(decrypted_text)
    return decrypted_texts


def write_decrypted_to_file(output_path, decrypted_texts):
    # 将解密后的数据写入新文件
    with open(output_path, 'w', encoding='utf-8') as file:
        for text in decrypted_texts:
            file.write(text + '\n')


if __name__ == '__main__':
    input_file = 'dmb/dmb104_mi_req.sh'
    output_file = 'dmb/dmb104_yuanwen_req.sh'
    sm4_key = '6707af3a3a7bc393ad4a547a5694c85f'  # 请替换为实际的 SM4 密钥

    # 读取文件
    print(input_file)
    base64_strings = read_dmb_file(input_file)
    print(base64_strings)

    # 解密数据
    decrypted_texts = decrypt_sm4(sm4_key, base64_strings)

    # 写入新文件
    write_decrypted_to_file(output_file, decrypted_texts)

    print(f"Decrypted data has been written to {output_file}")