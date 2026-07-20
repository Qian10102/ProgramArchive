import random
import sys
from xxsubtype import bench

# set 3 variables to record the number for win, tie and loss
win = 0
tie = 0
loss = 0

# set original parameter for the program
print("Rock, Paper, Scissors.")
print(f"{win} win, {tie} tie, {loss} loss.")
print("How many rounds do you want to play? Enter the number below: ")
num = int(input())

# main loop for the program
for i in range(num):
    while True:
        generate = random.randint(1,3)
        print("Enter your move: r for rock, p for paper, s for scissors, q for quit: ")
        PlayerChoice = input().lower()
        if PlayerChoice not in "rpsq":
            print("Type your choice in r p s or q!")
        else:
            break

# set the computer's move
    if generate == 1:
        ComputerChoice = "r"
    elif generate == 2:
        ComputerChoice = "p"
    elif generate == 3:
        ComputerChoice = "s"

# set the player's move and judge the output
    if PlayerChoice == "r":
        if ComputerChoice == "r":
            tie += 1
        elif ComputerChoice == "p":
            loss += 1
        elif ComputerChoice == "s":
            win += 1
    elif PlayerChoice == "s":
        if ComputerChoice == "s":
            tie += 1
        elif ComputerChoice == "r":
            loss += 1
        elif ComputerChoice == "p":
            win += 1
    elif PlayerChoice == "p":
        if ComputerChoice == "p":
            tie += 1
        elif ComputerChoice == "s":
            loss += 1
        elif ComputerChoice == "r":
            win += 1
    elif PlayerChoice == "q":
        sys.exit()

# print the output
    print(f"{win} win, {tie} tie, {loss} loss.")