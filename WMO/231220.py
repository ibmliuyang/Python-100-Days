import pandas as pd
import requests
import time
from bs4 import BeautifulSoup

# 要爬取的URL
base_url = "https://jinshuju.net/f/z6FGZw/s/6AVyo5?q%5B0%5D%5Bfield_1%5D=004600"
urls = [base_url + str(i).zfill(3) + "&embedded=&button=" for i in range(1, 229)]

# 空列表用于存储数据
data = []

# 每个请求之间的2秒延迟
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    print("url："+url)
    # 从HTML中提取所需数据
    tr_tags = soup.find_all("tr")
    extracted_data = []
    for tr in tr_tags:
        td_tags = tr.find_all("td")
        for td in td_tags:
            extracted_data.append(td.text.strip())

    # 将URL添加到提取的数据末尾
    extracted_data.append(url)
    data.append(extracted_data)

    # 延迟2秒后再发起下一个请求
    time.sleep(1)

# 将提取的数据转为DataFrame
df = pd.DataFrame(data)

# 将DataFrame保存到Excel文件
df.to_excel("/Users/ly/Downloads/3scraped_data.xlsx", index=False)