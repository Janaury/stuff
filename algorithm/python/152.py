while True:
    try:
        total, k = [int(i) for i in input().split()]
    except:
        break
    candies = [int(i) for i in input().split()]
    candies.sort()
    print(candies[k - 1])