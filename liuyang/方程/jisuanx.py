from sympy import *

x = symbols('x')

while True:
    s = int(input("输入总距离s:"))
    v1 = int(input("输入水流速度v1:"))
    a = solve([s/(x-v1)+s/(x+v1)-1], [x])
    print("船速：", a)


