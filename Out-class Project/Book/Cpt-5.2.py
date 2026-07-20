name_list = ["Admin","Kobe","Jorden","Jerry","Tom"]
name_log =  input().title()
length = len(name_list)
if name_log in name_list:
    if name_log == "Admin":
        print("Hello Admin, would you like to see the status report?")
        print("Yes or No?")
        confirm = input().title()
        if confirm == "Yes":
            for i in range(length):
                print(f"{name_list[i]} has logged in yesterday.")
        else:
            print("Thank you for logging in again.")
    else:
        print(f"Hello {name_log}, thank you for logging in!")
else:
    print(f"Hello {name_log}, please click the link below to register.")
    print("www.baidu.com")