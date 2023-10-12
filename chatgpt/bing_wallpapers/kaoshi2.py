price = 23  # 单价
money = int(input("请输入压岁钱数："))  # 输入压岁钱数，转换为整数类型
num = money // price  # 计算可以购买的书籍数量
remain = money % price  # 计算剩余的压岁钱数
print("可以购买{}本书，剩余{}元".format(num, remain))  # 输出结果
