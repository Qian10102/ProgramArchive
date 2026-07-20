current_users = ["Tom","Jerry","Betty","John","Rahim"]
new_users = list(input().split())
for users in new_users:
    users = users.title()
    if users in current_users:
        print("This name has been occupied. Please choose another one.")
    else:
        print("You have registered successfully!")