def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j

        # 交换找到的最小值与当前位置的元素
        arr[i], arr[min_index] = arr[min_index], arr[i]

# 示例
arr = [64, 25, 12, 22, 11]
selection_sort(arr)
print("选择排序后的数组:", arr)
