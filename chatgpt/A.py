# Python Program to Draw a Sunflower
import turtle
# Create a turtle object
t = turtle.Turtle()
# Set the background color
t.screen.bgcolor("black")
# Set the turtle speed
t.speed(10)
# Set the turtle color
t.color("yellow")
# Draw the petals
for i in range(36):
    t.circle(100, steps = 10)
    t.left(10)
# Draw the center of the flower
t.color("brown")
t.circle(20)
# Hide the turtle
t.hideturtle()