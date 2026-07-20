n = input()
count = 0
for s in n:
    s_str = str(s.lower())
    if s_str == 'a' or s_str == 'e' or s_str == 'i' or s_str == 'o' or s_str == 'u':
        count += 1
        print(count)
print(count)