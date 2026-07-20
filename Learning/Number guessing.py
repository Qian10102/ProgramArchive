import random
a = random.randint(1,100)
b = ""
while b != a:
    b = int(input("Please guess the number and enter your answer."))
    if b > a:
        print("It's too big!")
    elif b < a:
        print("It's too small!")
    elif b == a:
        print("Correct!")
        break