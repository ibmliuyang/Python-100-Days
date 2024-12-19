import os
import binascii

# 定义十六进制数据
hex_data = "2550 4446 2d31 2e34 0a25 e2e3 cfd3 0a34 2030 206f 626a 0a3c 3c2f 436f 6c6f 7253 7061 6365 2f44 6576 6963 6547 7261 792f 5375 6274 7970 652f 496d 6167 652f 4865"

# 将十六进制数据转换为二进制
binary_data = binascii.unhexlify(hex_data.replace(" ", ""))

# 获取文件夹路径
folder_path = '/Users/ly/Downloads/pycharm/'

# 列出文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 检查是否为文件
    if os.path.isfile(file_path):
        # 打开文件，以二进制模式读写
        with open(file_path, 'r+b') as file:
            # 获取文件的原始大小
            original_size = os.path.getsize(file_path)

            # 如果 binary_data 的长度大于原始文件大小，我们需要先读取文件的所有内容
            if len(binary_data) >= original_size:
                # 读取文件的全部内容
                file_content = file.read()

                # 将文件指针移到文件开头
                file.seek(0)

                # 写入二进制数据
                file.write(binary_data)

                # 将文件指针移到 binary_data 结束的位置
                file.seek(len(binary_data))

                # 将原来的文件数据写回文件
                file.write(file_content)
            else:
                # 如果 binary_data 的长度小于原始文件大小，我们只需写入 binary_data
                # 移动文件指针到文件开头
                file.seek(0)

                # 写入二进制数据
                file.write(binary_data)

                # 获取当前文件指针的位置
                current_position = file.tell()

                # 读取文件的剩余部分
                original_data = file.read()

                # 将文件指针移回到写入二进制数据后的位置
                file.seek(len(binary_data))

                # 将原来的文件数据写回文件
                file.write(original_data)

            # 获取文件的新大小
            new_size = os.path.getsize(file_path)

            # 输出处理信息
            print(f"Processed {filename}, new size: {new_size} bytes")