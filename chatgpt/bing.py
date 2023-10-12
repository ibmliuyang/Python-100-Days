import turtle

# 设置画笔颜色和填充颜色
turtle.color("black", "white")

# 绘制半圆
turtle.begin_fill()
turtle.circle(70, 90)
turtle.end_fill()

# 隐藏小海龟
turtle.hideturtle()

# 显示绘图窗口
turtle.done()
