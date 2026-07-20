N = int(input())
A = list(map(int,input().split()))
num = 0
for i in range(N):
    x = A[i]
    more = sum(1 for s in A if s >= x)
    less = sum(1 for s in A if s <= x)
    if less >= more:
        num = num + 1
print(num)