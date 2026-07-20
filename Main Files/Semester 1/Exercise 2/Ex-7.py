outcome_sum = 0
division_sum = 0
gpa_list = []
def gpa(x):
    if 60 <= x <= 100:
        gpa_single = 4 - 3 * ((100 - x) ** 2) / 1600
    elif 0 <= x < 60:
        gpa_single = 0
    gpa_list.append(gpa_single)

try:
    while True:
        a, b = map(int, input().split())
        gpa(a)
        outcome = gpa_list.pop()
        outcome_sum += outcome * b
        division_sum += b
except EOFError:
    pass

outcome_final = outcome_sum / division_sum
print(f"{outcome_final:.2f}")
