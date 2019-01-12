case_amount = int(input())

for i in range(case_amount):
    b,c,d = [int(x) for x in input().split()]
    result = c * 1 / (b * 1) * d
    print('{:.2f}'.format(result))
    