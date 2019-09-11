data = [[0 for i in range(10)] for i in range(10)]
while True:
    m,n = [int(i) for i in input().split()]
    if m == 0 and n == 0:
        break
    p = m
    for i in range(n):
        for j in range(i, -1, -1):
            data[n - 1 - j][i - j] = p
            p = p + 1
    
    for i in range(n):
        for j in range(i + 1):
            if(data[i][j] < 10):
                print(' ', end='')
            print(str(data[i][j]) + ' ', end='')
        print()
    print()
