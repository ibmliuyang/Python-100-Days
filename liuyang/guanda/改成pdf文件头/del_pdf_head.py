import os
import binascii

# 定义要删除的十六进制数据
hex_data_to_remove = "2550 4446 2d31 2e34 0a25 e2e3 cfd3 0a34 2030 206f 626a 0a3c 3c2f 436f 6c6f 7253 7061 6365 2f44 6576 6963 6547 7261 792f 5375 6274 7970 652f 496d 6167 652f 4865"

# 将十六进制数据转换为二进制
binary_data_to_remove = binascii.unhexlify(hex_data_to_remove.replace(" ", ""))

# 获取文件夹路径
folder_path = '/Users/ly/Downloads/pycharm/'

# 列出文件夹中的所有文件
for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)

    # 检查是否为文件
    if os.path.isfile(file_path):
        # 打开文件，以二进制模式读写
        with open(file_path, 'r+b') as file:
            # 读取文件的全部内容
            file_content = file.read()

            # 检查文件是否以要删除的数据开头
            if file_content.startswith(binary_data_to_remove):
                # 移除头部的数据
                remaining_content = file_content[len(binary_data_to_remove):]

                # 清空文件
                file.seek(0)
                file.truncate()

                # 将剩余的内容写回文件
                file.write(remaining_content)

                print(f"Processed {filename}")
            else:
                print(f"{filename} does not start with the specified data.")