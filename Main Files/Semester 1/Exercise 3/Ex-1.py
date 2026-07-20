def IsPerfectNumber(num):
    if num == 0:
        return False
    while num > 0:
        if num % 10 != 0 and num // 10 != 0:
            return False
        num = num // 10
    return True

def MultiplyNumbers(num):
    NumberList = []
    PerfectNumberList = []

    for i in range(n):
        for j in range(i+1,n):
            output_number = num[i] * num[j]
            NumberList.append(output_number)

    for num in NumberList:
        if IsPerfectNumber(num):
            PerfectNumberList.append(num)
    PerfectNumberList = set(PerfectNumberList)
    print(len(PerfectNumberList))

n = int(input())
num_int = list(map(int,input().split()))
MultiplyNumbers(num_int)