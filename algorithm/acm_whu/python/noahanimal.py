class ani():
    def __init__(self,space,point):
        self.space = space
        self.point = point

def calculate():
    for i in range(0, ta):
        for j in range(ts, -1, -1):
            if j >= al[i].space:
                tmp1 = pl[j]
                tmp2 = pl[j - al[i].space] + al[i].point
                if tmp2 > tmp1:
                    pl[j] = tmp2


pl = [0 for i in range(100001)]
while True:
    try:
        ta = int(input())
    except:
        break
    al = []
    for i in range(ta):
        space,point = [int(i) for i in input().split()]
        a = ani(space, point)
        al.append(a)
    ts = int(input())
    
    for i in range(100001):
        pl[i] = 0
    calculate()
    total_point = pl[ts]
    print(total_point)