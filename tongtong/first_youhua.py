import random

max_attempts = 3  # 可自定义尝试次数
target_num = random.randint(0, 10)

for attempt in range(max_attempts):
    guess_num = int(input(f"尝试 {attempt + 1}/{max_attempts} 输入你想要猜测的数字："))
    if guess_num == target_num:
        print("恭喜，你猜对了！")
        break
    elif guess_num > target_num:
        print("你猜的数大了")
    else:
        print("你猜的数小了")
else:
    print("三次机会用完了，没有猜中。正确答案是", target_num)
