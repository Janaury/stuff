case_amount = int(input())

for index in range(case_amount):
    num = int(input())
    x1 ,y1 = [int(i) for i in input().split()]
    x2, y2 = [int(i) for i in input().split()]
    x3 = abs(x1 - x2)
    y3 = abs(y1 - y2)
    if (x3 - y3) % 2 == 1 or (x3 - y3) % 2 == -1:
        print("Case {num}:\n-1\n".format(num = index + 1))
    else:
        if x3 > y3:
            result = x3
        else:
            result = y3 
        print("Case {num}:\n{result}\n".format(num = index + 1, result = result))