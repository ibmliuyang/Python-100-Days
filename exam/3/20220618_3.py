with open('书目.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        a = line.split("，")
        if a[0] == "水浒传" :
            print(a[1])
