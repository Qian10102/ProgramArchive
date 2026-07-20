a,b = map(int,input("请输入两个正整数：").split())
x = 1
while x > 0:
    x = (a % b)
    a = b
    b = x
else:
    print("最大公约数为",a)