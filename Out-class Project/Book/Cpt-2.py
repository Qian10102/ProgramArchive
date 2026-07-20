invitation = ["1","2","3"]
print(f"Mr.{invitation[2]} can't attend.")
invitation[2] = "4"
print(f"So I invite Mr.{invitation[2]} instead.")
for i in range(3):
    print(f"Dear Mr.{invitation[i]}, please come and have diner with me!")