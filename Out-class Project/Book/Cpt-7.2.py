un_verified_user = ["Thomas", "Max", "Philippe"]
verified_user = []
while len(un_verified_user) != 0:
    verifying_user = un_verified_user.pop()
    verified_user.append(verifying_user)
    print(f"User {verifying_user} has been verified \n{len(un_verified_user)} users remaining to be verified.")
    if len(un_verified_user) == 0:
        print("All users have been verified successfully.")