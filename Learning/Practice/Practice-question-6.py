def find_max(numbers):
    if numbers:
        numbers.sort()
        print(numbers[len(numbers)-1])
    else:
        print(None)

numbers_list = []
find_max(numbers_list)