class point():
    def __init__(self,x,y):
        self.x = x
        self.y = y


def testSymmetry():
    last_axis = -1
    while len(point_list) > 0:
        axis = -1
        base = point_list[0].x
        min_y = point_list[0].y
        max_y = point_list[0].y
        min_num = 0
        max_num = 0
        for i in range(1,len(point_list)):
            if point_list[i].x == base:
                if point_list[i].y < min_y:
                    min_y = point_list[i].y
                    min_num = i
                elif point_list[i].y > max_y:
                    max_y = point_list[i].y
                    max_num = i

        if max_num != min_num:
            axis = (max_y + min_y) / 2
            if max_num > min_num:
                f = max_num
                s = min_num
            else:
                f = min_num
                s = max_num
            point_list.pop(f)
            point_list.pop(s)
        else:
            axis = max_y
            point_list.pop(max_num)
        if last_axis != -1 and abs(axis - last_axis) > 1e-9:
            return -2
        else:
            last_axis = axis
    return 0

while True:
    try:
        total_point = int(input())
    except:
        break
    point_list = []
    for i in range(total_point):
        x,y = [int(i) for i in input().split()]
        point_list.append(point(x,y))
    
    axis = testSymmetry()
    if axis == -2:
        print("NO")
    else:
        print("YES")

