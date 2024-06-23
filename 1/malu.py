import math

v = 1.2  # 设置行走速度
t0 = 1  # 设置行人反应时长
s = int(input("请输入马路的宽度（米）："))
t = s / v + t0  # 计算绿灯最短时长公式

if t % 1 != 0:  # 判断 t 是否为整数
    print(math.ceil(t))  # t 不是整数，向上取整
else:
    print(int(t))
