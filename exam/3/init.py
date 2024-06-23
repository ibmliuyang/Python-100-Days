import os

# 指定目录路径
directory = "/Users/ly/ynworkspace/Python-100-Days/exam/3/"

# 循环创建文件
for i in range(4, 36):
    # 构造文件名
    filename = f"20220618_{i}.py"
    # 构造文件内容
    content = "print('hello')"

    # 构造完整文件路径
    file_path = os.path.join(directory, filename)

    # 创建并写入文件
    with open(file_path, 'w') as file:
        file.write(content)
