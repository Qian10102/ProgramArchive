import random
total = int(input())
total_award = []
for i in range(1,total+1):  #生成总票号表
    total_award.append(i)
random.shuffle(total_award) #随机打乱总票号表
print(total_award[:2])      #输出特等奖名单
print(total_award[2:8])     #输出一等奖名单
print(total_award[8:18])    #输出二等奖名单
print(total_award[18:38])   #输出三等奖名单