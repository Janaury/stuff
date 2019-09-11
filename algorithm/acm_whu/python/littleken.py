def calculate(p):
    prefix = p * p
    rp = 1
    last_p = 1
    for i in range(1, 100000):
        last_p = 2 * last_p * (1 - p) * p
        rp = rp + last_p
    
    return rp * prefix
        
case_amount = int(input())
for i in range(case_amount):
    percent = int(input()[:-1]) / 100
    result = calculate(percent) * 100
    print("{num:.2f}%".format(num=result))
