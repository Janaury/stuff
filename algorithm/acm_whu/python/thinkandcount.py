import time

def statistic():
    for i in range(rm):
        line = [0 for i in range(cm)]
        sw_count = 0
        for j in range(cm-1, -1, -1):
            if board[i][j] is 'w':
                sw_count = sw_count + 1
                line[j] = sw_count
            else:
                sw_count = 0
        sw_line.append(line)

def countFrom(rs,cs):
    total = 0
    re = rm
    ce = sw_line[rs][cs]
    for i in range(rs, re):
        if sw_line[i][cs] < ce:
            ce = sw_line[i][cs]
        total = total + ce
        if ce is 0:
            break
    return total

while True:
    try:
        a = input()
    except:
        break
    rm, cm = [int(i) for i in a.split()]
    board = []
    count = 0
    for i in range(rm):
        row = input()
        board.append(row)
    sw_line = []
    statistic()
    for i in range(rm):
        for j in range(cm):
            part_count = countFrom(i,j)
            count = count + part_count
    print(count)

