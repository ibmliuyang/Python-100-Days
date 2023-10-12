import turtle
# 画三角形
turtle.pensize(2)
for i in range(100):
    turtle.forward(50)
    turtle.left(120)
    turtle.forward(50)
    turtle.left(120)
    turtle.forward(50)
    turtle.left(120)
    turtle.penup()
    turtle.forward(60)
    turtle.pendown()
# 画圆形
turtle.pensize(2)
for i in range(100):
    turtle.circle(25)
    turtle.penup()
    turtle.forward(60)
    turtle.pendown()
# 画正方形
turtle.pensize(2)
for i in range(100):
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.forward(50)
    turtle.left(90)
    turtle.penup()
    turtle.forward(60)
    turtle.pendown()
turtle.done()