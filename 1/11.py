f = open('书目.csv','r')
c=[]
for i in f:
	c.append(i.strip('\n').split(','))
f.close()
print(c)