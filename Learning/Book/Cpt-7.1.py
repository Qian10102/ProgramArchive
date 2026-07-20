prompt = "Please enter the ingredient you choose (enter 'end' to end): "
choose = ""
ingredients = []
while choose != "end":
    choose = input(prompt)
    print(f"You have chosen to add {choose} in your pizza.")
    if choose == "end":
        continue
    ingredients.append(choose)
print(f"Your pizza has the ingredients below: \n{ingredients}")