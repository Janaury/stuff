import math
while True:
    try:
        n = int(input())
    except:
        break

    m = int(math.sqrt(n))
    print(m)