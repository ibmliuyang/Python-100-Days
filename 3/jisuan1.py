from fractions import Fraction
import re

def evaluate_expression(expression):
    # 移除空格
    expression = expression.replace(" ", "")

    # 匹配括号内的表达式
    while "(" in expression:
        expression = re.sub(r"\(([^\(\)]+)\)", lambda m: str(evaluate_expression(m.group(1))), expression)

    # 分割表达式中的运算符和操作数
    operators = re.findall(r"[-+*/]", expression)
    operands = re.split(r"[-+*/]", expression)

    # 将操作数转换为分数对象
    operands = [Fraction(operand) for operand in operands]

    # 逐步计算表达式
    result = operands[0]
    for i in range(len(operators)):
        operator = operators[i]
        operand = operands[i+1]
        if operator == "+":
            result += operand
        elif operator == "-":
            result -= operand
        elif operator == "*":
            result *= operand
        elif operator == "/":
            result /= operand

        print("Step {}: {} {} {} = {}".format(i+1, result, operator, operand, result))

    return result

# 使用示例
expression = "22 / 9 / ((89 / 12 - 5.25) / 1.5 + 10 * 5 / 18)"
final_result = evaluate_expression(expression)
print("Final Result:", final_result)