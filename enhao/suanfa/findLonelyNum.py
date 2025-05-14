def find_unique_number(cards):
    if len(cards) == 1:
        return cards[0]
    cards.sort()
    i = 0
    while i < len(cards) - 1:
        if cards[i] != cards[i + 1]:
            return cards[i]
        i += 2
    return cards[-1]


# 测试样例
print(find_unique_number([1, 1, 2, 2, 3, 3, 4, 5, 5]))
print(find_unique_number([0, 1, 0, 1, 2]))
print(find_unique_number([7, 3, 3, 7, 10]))