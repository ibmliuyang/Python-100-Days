import os
import json

from liuyang.guanda.sm4.sm4utils import SM4Util


def process_files(directory):
    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            filepath = os.path.join(directory, filename)
            new_filename = filename.rsplit('.', 1)[0] + '.txt'
            new_filepath = os.path.join(directory+"_jiemi", new_filename)

            # 读取文件
            with open(filepath, 'r') as file:
                content = file.read()

            # 解析JSON
            try:
                data = json.loads(content)
                response_data = data['body']
                response_data = json.loads(response_data)
                data_value = response_data['Response']['Data']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error processing {filename}: {e}")
                continue




            # 修改数据
            modified_data = SM4Util.dec(data_value)
            print(modified_data)

            # 更新JSON
            response_data['Response']['Data'] = modified_data
            data['body'] = json.dumps(response_data)

            # 写入新文件
            with open(new_filepath, 'w') as new_file:
                new_file.write(json.dumps(data, indent=4))


# 指定目录
directory = 'message'
process_files(directory)