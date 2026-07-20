def FrequencyNumbers(n,num_list):
    count_list = []
    output_list = []
    output_list_set = []
    association = {}
    for i in num_list:
        count = sum(1 for num in num_list if num == i)
        association[i] = count
    for i in association.values():
        count_list.append(i)
    count_list.sort(reverse=True)
    for i in range(n):
        number_key = count_list[i]
        for key, values in association.items():
            if values == number_key:
                output_list.append(key)
    output_list.sort()
    for i in output_list:
        if i not in output_list_set:
            output_list_set.append(i)
    if n <= len(output_list_set):
        output_list_set = output_list_set[:n]
    result = ",".join(map(str, output_list_set))
    print(result)

n = int(input())
num_list = list(map(int,input().split()))
FrequencyNumbers(n,num_list)