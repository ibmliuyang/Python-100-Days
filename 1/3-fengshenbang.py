with open('/data/书籍存单csv”', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        a = line.strip().split(",")
        if a[0] == "封神榜":
            print(f"《封神榜》的价格为：{a[1]}元")
