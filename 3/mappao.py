def bubble_sort(arr):
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n-1):
        # 最后 i 个元素已经排好序，不需要再比较
        for j in range(0, n-i-1):
            # 如果当前元素大于下一个元素，则交换它们
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]

# 测试代码
arr = [7, 2, 9, 6, 4, 5]
bubble_sort(arr)
print("排序后的数组：", arr)