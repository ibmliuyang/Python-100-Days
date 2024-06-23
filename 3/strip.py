f = open ("city.csv", "r")
ls=[]
for line in f:
    ls.append (line.strip("\n").split(","))
    print(type(line))
f.close()
print (ls)
ls.remove(['1', '3', '4'])
print (ls)
print (type(ls))

