f = open('身体素质.csv', 'r')
a = []
for i in f:
    a.append(i.strip('\n').split(','))
f.close
for x in a:
    line=''
    for y in x:
        line = line + y+'\t'
    print(line)
