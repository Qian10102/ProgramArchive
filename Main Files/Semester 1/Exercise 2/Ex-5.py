A = int(input())
def rabbit_pairs(months):
    if months == 1:
        return 1
    elif months == 2:
        return 2
    else:
        fib = [0] * (months + 1)
        fib[1] = 1
        fib[2] = 2
        for i in range(3, months + 1):
            fib[i] = fib[i - 1] + fib[i - 2]
        return fib[months]

result = rabbit_pairs(A)
print(result)
