import requests
import time
from email.mime.text import MIMEText
import smtplib
import logging

# 配置日志

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logfile.log',
                    filemode='a')  # 'a' 表示追加模式

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
        response = requests.get('http://sjzjyj.sjz.gov.cn/a/zwgk/tzgg/index.html')
        response.encoding = 'utf-8'
        content = response.text
        if last_content != content:
            # 使用logging.info代替print输出当前时间
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 内容发生变化，发送邮件
            logging.info("Content has changed! content：" + content)
            send_email("发公告了！！！", content)
            last_content = content
        else:
            logging.info(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            logging.info("No change detected.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")
    time.sleep(60)  # 等待1分钟