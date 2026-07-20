output = 0
answer = []
num = int(input())
activation = True
while activation:
    remainder = num % 2
    quotient = num // 2
    answer.append(remainder)
    while quotient >= 2:
        remainder = quotient % 2
        quotient = quotient // 2
        answer.append(remainder)
        if quotient <= 1:
            activation = False
            answer.append(quotient)
answer.reverse()
for i in range(len(answer)):
    digit = int(answer[i]) * (10 ** (len(answer)-(i+1)))
    output += digit
print(output)