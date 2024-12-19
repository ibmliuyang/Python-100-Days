import requests
from bs4 import BeautifulSoup
import codecs

# 目标URL
url = 'https://item.jd.com/100133275326.html'

# 发送HTTP请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

    print(soup.prettify())
    # 查找class为"price"的元素
    price_element = soup.find(class_='price')

    if price_element:
        # 获取价格内容
        price = price_element.get_text(strip=True)

        # 打印价格
        print(f'Price: {price}')
    else:
        print('Price element not found')
else:
    print(f'Failed to retrieve the page. Status code: {response.status_code}')

# 示例处理转义序列
escaped_string = '\\xe7\\xb4\\xa2\\xe5\\xb0\\bc\\xe7\\x94\\xb5\\xe8\\xa7\\x86'

# 使用codecs模块解码转义序列
decoded_string = codecs.escape_decode(escaped_string)[0].decode('utf-8')

print(f'Decoded string: {decoded_string}')