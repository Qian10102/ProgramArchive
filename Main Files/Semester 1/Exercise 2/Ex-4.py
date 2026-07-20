import math
output_list = []
a,b,c = map(float,input().split())
delta = (b ** 2) - 4 * a * c

if delta < 0:
    print("no real roots")
elif delta >= 0:
    delta_modify = math.sqrt(delta)
    root_a = (-b + delta_modify) / (2 * a)
    root_b = (-b - delta_modify) / (2 * a)
    if root_a > root_b:
        root_a, root_b = root_b, root_a
    print(f"{root_a:.6f} {root_b:.6f}")