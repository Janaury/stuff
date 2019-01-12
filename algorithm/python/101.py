
def cni2(n,i):
    result = 1
    for j in range(0, i):
        result = result * (n-j) // (j+1)

    return result

def doCalculate(step, case, dx, dy):
    result = 0
    for i in range(case + 1):
        result = result + cni2(step, dx + i) * cni2(step - dx - i, dy + case - i) * cni2(case, i)
    return result

def calculateAll():
    dx = int(abs(x2 - x1))
    dy = int(abs(y2 - y1))
    min_step = dx + dy
    extra_step = step - min_step
    case = int(extra_step / 2)
    result = 0
    if min_step > step:
        return result
    else:
        return doCalculate(step, case, dx, dy)


case_amount = int(input())
for index in range(case_amount):
    x1,y1,x2,y2,step = [int(i) for i in input().split()]
    result = calculateAll()
    print(result)