from sympy import symbols, Eq, solve

# 定义变量
x, y = symbols('x y')

# 定义方程组
equation1 = Eq(x/(x+y+1000), 1/5)
equation2 = Eq((x+1000)/(x+y+2000), 1/3)

# 解方程组
solutions = solve((equation1, equation2), (x, y))

# 输出解
print(solutions)
