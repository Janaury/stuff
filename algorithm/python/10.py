# 最大的数的2^(n - 1)次方
while True:
    size = int(input())
    if size == 0:
        break
    collection = [int(i) for i in input().split()]
    collection.sort(reverse = True)
    sum = collection[0]
    for i in range(size - 1):
        sum = (sum * 2) % 2006
    if sum < 0:
        sum = sum + 2006
    print(sum)

