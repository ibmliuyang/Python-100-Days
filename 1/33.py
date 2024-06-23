try:
	x=int(input())
	y=int(input())
	n=x%y
	print(n)
except ValueError:
	print('ValueError!')
except ZeroDivisionError:
	print('ZeroDivisionError!')
except:
	print('Other error!')