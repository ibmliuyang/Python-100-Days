import turtle

boat = turtle.Turtle()

boat.pencolor("blue")
boat.pensize(3)

boat.penup()
boat.goto(-100, -100)

boat.pendown()
boat.forward(200)
boat.left(120)
boat.forward(200)
boat.left(120)
boat.forward(200)

boat.right(60)
boat.forward(150)
boat.right(90)
boat.forward(50)

turtle.done()
