import turtle

# 设置画笔颜色和填充颜色
turtle.color("pink", "pink")

# 绘制花瓣
turtle.begin_fill()
for i in range(2):
    turtle.circle(70, 90)
    turtle.circle(70/2, 90)
turtle.circle(70, 90)
turtle.circle(70/2, 45)
turtle.right(105)
turtle.circle(-70/2, 90)
turtle.left(30)
turtle.circle(-70, 90)
turtle.circle(-70/2, 45)
turtle.end_fill()

# 隐藏小海龟
turtle.hideturtle()

# 显示绘图窗口
turtle.done()
