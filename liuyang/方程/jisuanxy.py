from sympy import *

x, y= symbols('x y')

#a = solve([3*x+2*y+5*z-2, x-2*y-z-6, 4*x+2*y-7*z-30], [x, y, z])
a = solve([x+y-115/60, 4*x+36*y-21], [x, y])

print(a)

