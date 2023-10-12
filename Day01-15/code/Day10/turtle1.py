import turtle

# 设置画笔颜色和填充颜色
turtle.pencolor("pink")
turtle.left(105)
for i in range(5):
    turtle.circle(70, 90)
    turtle.left(90)
    turtle.circle(70, 90)
    turtle.left(60)

# 隐藏小海龟
turtle.hideturtle()

# 显示绘图窗口
turtle.done()
