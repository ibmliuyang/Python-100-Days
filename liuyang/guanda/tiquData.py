import os
import json

# 定义目录路径
directory = '/Users/ly/Documents/ggnl_response'

# 遍历目录下的所有文件
for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        filepath = os.path.join(directory, filename)

        # 读取文件内容
        with open(filepath, 'r') as file:
            try:
                data = json.load(file)
                # 解析嵌套的JSON字符串
                body = data.get('body', '{}')
                inner_data = json.loads(body)

                # 提取 "Data" 字段
                data_content = inner_data.get('Response', {}).get('Data', '')

                print(f"In file {filename}, Data content is: {data_content}")
            except json.JSONDecodeError:
                print(f"Failed to decode JSON in {filename}.")
            except Exception as e:
                print(f"An error occurred while processing {filename}: {e}")