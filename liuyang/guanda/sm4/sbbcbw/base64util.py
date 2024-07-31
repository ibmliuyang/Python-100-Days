import base64


def decode_base64_file(input_filename, output_filename):
    try:
        # 读取Base64编码的文件
        with open(input_filename, 'rb') as file:
            encoded_data = file.read()

        # Base64解码
        decoded_data = base64.b64decode(encoded_data)

        # 写入解码后的数据到新文件
        with open(output_filename, 'wb') as file:
            file.write(decoded_data)

        print(f"File '{input_filename}' has been successfully decoded and saved as '{output_filename}'.")

    except FileNotFoundError:
        print(f"Error: The file '{input_filename}' was not found.")

    except Exception as e:
        print(f"An error occurred: {e}")


# 调用函数
decode_base64_file('sbbcbw_base64.txt', 'sbbcbw_yuan.txt')