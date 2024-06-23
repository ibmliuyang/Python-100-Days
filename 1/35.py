shuig=['苹果，香蕉，桃子','西瓜']
f=open('shuiguo.csv','w')
f.write(','.join(shuig)+'\n')
f.close()