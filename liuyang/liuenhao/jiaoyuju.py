import requests
import time
from email.mime.text import MIMEText
import smtplib

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
            # 打印当前时间
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            # 内容发生变化，发送邮件
            print("Content has changed! content：" + content)
            send_email("Website Content Changed", content)
            last_content = content
        else:
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            print("No change detected.")
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(60)  # 等待1分钟