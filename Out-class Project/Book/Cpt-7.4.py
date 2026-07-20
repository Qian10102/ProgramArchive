i = 0
pet = {}
pet_information = []
activation = True
def animal(owner_name, animal_name, animal_type):
    """关联人、宠物名称和宠物种类"""
    print(f"{owner_name} has a(n) {animal_type} named {animal_name}. {owner_name} love {animal_name}")

while activation:
    owner_name = input("Please enter owner's name:").title().strip()
    pet_name = input("Please enter pet's name: ").title().strip()
    pet_type = input("Please enter pet's type: ").lower().strip()
    confirm = input("Do you want to input more? (yes/no) ").lower().strip()
    pet_information.append(pet_name)
    pet_information.append(pet_type)
    pet[owner_name] = pet_information
for owner_name in pet:
    pet_name = pet_information[i]
    pet_type = pet_information[i+1]
    i = i+2
    animal(owner_name,pet_name,pet_type)