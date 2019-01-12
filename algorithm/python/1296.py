while True:
    n = int(input())
    if n == 0:
        break
    if n % 2 == 0:
        print('No Solution!')
    else:
        print(n - 1)