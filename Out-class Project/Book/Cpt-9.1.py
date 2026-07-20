class Dog:
    """尝试模拟小狗"""
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def sit(self):
        print(f"Your dog {self.name} is now sitting.")

    def roll_over(self):
        print(f"Your dog {self.name} is now rolling over.")

name = input("Enter your dog's name: ")
age = int(input("Enter your dog's age: "))
dog = Dog(name, age)
print(f"The class of your dog named {name} has been established.")
guidance = input("Choose from the two methods below: s for sit and r for roll over")
while 1 == 1:
    if guidance == "s":
        dog.sit()
        break
    elif guidance == "r":
        dog.roll_over()
        break
    else:
        guidance = input("Choose and enter between s and r please!")
        continue