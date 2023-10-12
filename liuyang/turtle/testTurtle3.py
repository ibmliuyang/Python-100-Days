from turtle import *

print(pos())
color('yellow', 'red')
begin_fill()
speed(100)
while True:
    forward(200)
    left(150)
    print("pos()", pos())

    print("abs(pos())", abs(pos()))
    if abs(pos()) < 1:
        break
goto(0, 0)


end_fill()

done()