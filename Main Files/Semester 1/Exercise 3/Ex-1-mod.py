def is_perfect_number(num):
    non_zero_count = 0
    while num > 0:
        digit = num % 10
        if digit != 0:
            non_zero_count += 1
        num //= 10
    return non_zero_count == 1

def count_perfect_product_pairs(n, arr):
    count = 0
    for i in range(n):
        for j in range(i + 1, n):
            product = arr[i] * arr[j]
            if is_perfect_number(product):
                count += 1
    return count

n = int(input())
arr = list(map(int, input().split()))
result = count_perfect_product_pairs(n, arr)
print(result)
