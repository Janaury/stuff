case_amount = int(input())

for index in range(case_amount):
    n = int(input())
    n = n % 7
    if n <= 1:
        print("Dzs")
    else:
        print("Sproblvem")