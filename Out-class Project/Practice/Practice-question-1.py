original_list = []
def fizzbuzz(n):
    for i in range(1,n+1):
        if i % 3 == 0 and i % 5 == 0:
            original_list.append('FizzBuzz')
        elif i % 3 == 0 and i % 5 != 0:
            original_list.append('Fizz')
        elif i % 3 != 0 and i % 5 == 0:
            original_list.append('Buzz')
        else:
            original_list.append(i)
    print(original_list)

n = int(input())
fizzbuzz(n)