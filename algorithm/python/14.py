# 每个test case间用空行隔开了，题目输入格式中没有提到
while True:
    try:
        x1, x2, x3 = [int(i) for i in input().split()]
        y1, y2, y3 = [int(i) for i in input().split()]
        z1, z2, z3 = [int(i) for i in input().split()]
    except:
        break
    result = abs(x1 * (y2 * z3 - y3 * z2) - y1 * (x2 * z3 - x3 * z2) + z1 * (x2 * y3 - x3 * y2))
    print("{:.2f}".format(result))
    try:
        input()
    except:
        break
   
    