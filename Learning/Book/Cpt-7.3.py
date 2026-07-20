responses = {}
activation = True
while activation:
    name = input("Please enter your name: ")
    response_detail = input("Which mountain do you like to climb: ").split()
    verify = input("Would you like to ask other people to respond? (yes/no) ")
    responses[name] = response_detail
    verify = verify.lower()
    if verify == "no":
        activation = False
for name, response_detail in responses.items():
    print(f"Mr. {name} would like to climb the mountain above:")
    for response in response_detail:
        print(response)