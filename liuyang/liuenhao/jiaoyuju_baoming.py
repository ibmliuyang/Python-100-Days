import requests
import time
from email.mime.text import MIMEText
import smtplib
import logging

# 配置日志

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='gongbu48.log',  # 日志文件名
                    filemode='a')  # 文件打开模式，'a'表示追加

EMAIL_ADDRESS = '393670@qq.com'  # 发件人邮箱
EMAIL_PASSWORD = 'nndcfvflltxxcaae'  # 发件人邮箱密码或应用密码
RECIPIENT_EMAIL = '393670@qq.com'  # 收件人邮箱
SMTP_SERVER = 'smtp.qq.com'  # SMTP服务器
SMTP_PORT = 587  # SMTP端口
last_content = None

def send_email(subject, message):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, [RECIPIENT_EMAIL], msg.as_string())

while True:
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
        url = 'https://sjzzs.shidajy.com/smsySchoolApi/assignAdmissions/getSchoolList'

        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        content = response.text
        if last_content != content:
            # 使用logging.info代替print输出当前时间
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 内容发生变化，发送邮件
            logging.info("48公布了！！: " + content)
            send_email("48公布了！！: ", content)
            last_content = content
        else:
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            logging.info("网站没有变化，没有开始.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    time.sleep(62)  # 等待1分钟