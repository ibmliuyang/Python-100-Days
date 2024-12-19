import requests
from bs4 import BeautifulSoup

# 目标URL
url = 'https://item.jd.com/100133275326.html'

# 发送HTTP请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 解析HTML
    soup = BeautifulSoup(response.content, 'html.parser')

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