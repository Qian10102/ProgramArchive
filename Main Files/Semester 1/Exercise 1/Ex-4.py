n,l,r = map(int,input().split())
x = list(map(int,input().split()))
num = 0
for i in x:
    if i % 2 == 0 and l <= i <= r:
        num = num + 1
print(num)
