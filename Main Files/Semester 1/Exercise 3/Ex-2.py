n = int(input())
a = list(map(int, input().split()))
mod = 10**9 + 7
S = 0
for i in range(1, n + 1):
    val = a[i - 1]
    x = (i * (i + 1) // 2) % mod
    y = (n - i + 1) % mod
    contrib = val * x % mod
    contrib = contrib * y % mod
    S = (S + contrib) % mod
print(S)