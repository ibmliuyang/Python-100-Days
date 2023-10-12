from sympy import *

x, y = symbols('x y')
# a = solve([3*x+2*y+5*z-2, x-2*y-z-6, 4*x+2*y-7*z-30], [x, y, z])

a = solve([10+30*x-2/3*x*y, 10+30*x-2/3*y-2*x*y], [x, y])
print(a)
