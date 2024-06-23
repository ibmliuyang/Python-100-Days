lst = [8, 9, 10, 12, 13, 14, 16, 17, 25, 27]
hm = int(input('请输入书本号码'))

# ①
n = len(lst)
i, j = 0, len(lst) - 1
b = -1

# ②
while i <= j:
    # ③
    m = (i + j) // 2
    if lst[m] == hm:
        b = m
        break
    elif hm > lst[m]:
        # ④
        i = m + 1
    else:
        j = m - 1

if b == -1:
    print('要查找的书号[' + str(hm) + ']不在列表lst中。')
else:
    # ⑤
    print('要查找的书号[' + str(hm) + ']排第' + str(b + 1) + '。')
