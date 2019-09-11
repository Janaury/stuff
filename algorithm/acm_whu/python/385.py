case_amount = int(input())

for index in range(case_amount):
    a, b = [int(i) for i in input().split()]
    result = (a-1)*(b-1)-1
    print(result)