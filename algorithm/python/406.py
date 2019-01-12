while True:
    try:
        a, b = [int(i) for i in input().split()]
    except:
        break
    if a == 0:
        print(0)
    else:
        print(int(b/a/2.00+0.5-0.000001))