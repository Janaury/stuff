data = [0 for i in range(26)]

data[0] = 1
data[1] = 1
for i in range(2, 26):
    for j in range(i - 1, -1, -1):
        data[i] = data[i] + data[j] * data[i - 1 -j]

while True:
    try:
        num = int(input())
    except:
        break
    
    if num != 0:
        print(data[int(num / 2)])
    else:
        print(0)