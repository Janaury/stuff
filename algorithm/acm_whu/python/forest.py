import re
names = ["littleken","knuthocean","dongfangxu","zap","kittig","robertcui","forest","flirly"]
case_amount = int(input())
for i in range(case_amount):
    amount = [0 for i in range(len(names))]
    s = input()
    for j in range(len(names)):
        amount[j] = len(re.findall(names[j],s))
    max = []
    tmp = 0
    for j in range(len(names)):
        if amount[j] > tmp:
            max = []
            max.append(j)
            tmp = amount[j]
    print(names[max[0]])

