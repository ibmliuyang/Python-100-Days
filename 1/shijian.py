from datetime import datetime, timedelta

# 获取今天的日期
today = datetime.now()

# 设定目标日期为2024年7月10日
target_date = datetime(2024, 7, 10)

# 计算两个日期之间的差距
days_remaining = (target_date - today).days

# 打印出每个月份的日期
current_date = today
while current_date <= target_date:
    print(current_date.strftime("%Y年%m月%d日"))
    current_date += timedelta(days=1)

print(f"\n从今天到2024年7月10日还有 {days_remaining} 天。")
