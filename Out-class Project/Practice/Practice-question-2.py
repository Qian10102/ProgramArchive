value = []
def fibonacci(n):
    for i in range(n):
        if i == 0:
            value.append(0)
        elif i == 1:
            value.append(1)
        else:
            value_add = value[i - 1] + value[i - 2]
            value.append(value_add)
    print(value)

n = int(input())
fibonacci(n)