while True:
    try:
        animal_amount = int(input())
    except:
        break
    cost_list = []
    for i in range(8):
        line = [int(x) for x in input().split()]
        cost_list.append(line)
    min_list = []
    for i in range(animal_amount):
        min = 100000
        for j in range(8):
            if cost_list[j][i] < min:
                min = cost_list[j][i]
        min_list.append(min)
    result = 0
    for item in min_list:
        result = result + item
    print(result)
