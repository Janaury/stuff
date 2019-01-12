while True:
    try:
        a, b = [int(i) for i in input().split()]
    except:
        break
    tmp = [int(i) for i in input().split()]
    tmp.sort()
    min_v = tmp[0]

    print(int(b/min_v))

