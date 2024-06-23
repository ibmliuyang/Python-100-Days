import random
num = random.randint(0,10)
guess_num = int(input("输入你想要猜测的数字："))
if guess_num == num:
    print("恭喜，第一次就猜对了")
else:
    if guess_num > num:
        print("你猜的数大了")
    else:
        print("你猜的数小了")
    guess_num = int(input("再次输入你想要猜测的数字："))
    if guess_num == num:
            print("恭喜，第二次猜对了")
    else:
        if guess_num > num:
            print("你猜的数大了")
        else:
            print("你猜的数小了")
        guess_num = int(input("第三次输入你想要猜测的数字："))
        if guess_num == num:
            print("恭喜，第三次猜对了")
        else:
            print("三次机会用完了，没有猜中")