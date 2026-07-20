def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def goldbach_conjecture(n):
    primes = [i for i in range(2, n) if is_prime(i)]
    results = []

    for a in primes:
        if a <= n / 2:
            b = n - a
            if b in primes:
                results.append((a, b))

    for a, b in results:
        print(f"{n} = {a} + {b}")

n = int(input())
goldbach_conjecture(n)