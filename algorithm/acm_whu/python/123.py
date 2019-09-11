while True:
    try:
        n = int(input())
    except:
        break

    if n == 1:
        print(n)
    else:
        print(n * 2 - 2)