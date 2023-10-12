# 导入pandas库
import pandas as pd

# 读取原始excel文件，文件名为d:/1.xls
df = pd.read_excel("/Users/ly/Downloads/1.xls")

print(df["1"])
# 计算c、d两列的合计，并添加到新的一列，命名为total


# 选择要保存的列，即total列


# 写入新的excel文件，文件名为d:/2.xls
