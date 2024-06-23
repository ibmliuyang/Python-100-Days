from fractions import Fraction
from math import floor

def to_mixed_number(fraction):
    whole_part = floor(fraction)
    fraction_part = fraction - whole_part
    if fraction_part == 0:
        return str(whole_part)
    else:
        return f"{whole_part} {fraction_part.numerator}/{fraction_part.denominator}"

# 例子：表示3/2为带分数
fraction = Fraction(3, 2)
mixed_number = to_mixed_number(fraction)
print(mixed_number)  # 输出: 1 1/2
print(mixed_number*2)  # 输出: 1 1/2
