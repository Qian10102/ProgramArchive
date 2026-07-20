import math                         #导入数学库，进行向上取整操作
a,b = input().split()               #a,b为输入的样本
if int(b) == 0:                     #判断每天是否能存钱，若不能，则输出-1
    print(-1)
else:                               #若可以存钱，则输出“a/b”的取整
    print(math .ceil(int(a)/int(b)))