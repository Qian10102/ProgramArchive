degree_f = int(input())
degree_c = (degree_f - 32) * 5 / 9
d_str = str(degree_c)
d_place = len(d_str.split(".")[1])
if d_place < 2:
    print_degree_c = format(degree_c, '.2f')
elif d_place >= 2:
    print_degree_c = round(degree_c,2)
print(print_degree_c)