import sys
import json
import base64

# gpus = sys.argv[1]  # 这一行被注释掉了
gpus = 'sbzf_req'

input_file_name = gpus + '.json'
print('读取文件：' + input_file_name)

with open(input_file_name, 'r', encoding='utf-8') as f:
    org_data = json.loads(f.read())

# 检查 ywbw 下的数据中是否有 sbsj 键，并进行 Base64 编码
if 'ywbw' in org_data:
    for item in org_data['ywbw']:
        if 'sbsj' in item:
            # 将 sbsj 转换为 JSON 字符串
            sbsj_str = json.dumps(item['sbsj'], ensure_ascii=False)
            # 对 JSON 字符串进行 Base64 编码
            item['sbsj'] = base64.b64encode(sbsj_str.encode('utf-8')).decode('utf-8')

result = {
    "url": "15.250.76.98:15050/access/sandbox/v2/invoke/206001/SBZF",
    "body": json.dumps(org_data, ensure_ascii=False),
    "ylbm": "206001",
    "nlbm": "206001",
    "sydwptbh": "17507d5e6814dea7aa99",
    "jrdwptbh": "174ba8fa83cf8ce21a9d",
    "fwbm": "SBZF",
    "content": "application/json",
    "host": "EBIS-GCH-MicroBusiness",
    "extCebFtrancode": "SG01",
    "key": "8d206a83e1352874d12a16cc6a4a8332",
    "extCeblnstno": "01060001"
}

output_file_name = gpus + '.json.txt'
print('写出文件：' + output_file_name)

with open(output_file_name, 'w', encoding='utf-8') as f:
    f.write(json.dumps(result, indent=4, ensure_ascii=False))