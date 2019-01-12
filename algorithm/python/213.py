
def findCow(used,pos):
    if pos == cow:
        return 0
    elif used >= max_used:
        return max_used
    elif pos == 0:
        tmp1 = findCow(used + 1, 2 * pos)
        tmp2 = findCow(used + 1, pos + 1)
        if tmp1 > tmp2:
            return tmp1 + 1
        else:
            return tmp2 + 1
    elif pos < cow:
        tmp1 = findCow(used + 1, 2 * pos)
        tmp2 = findCow(used + 1, pos + 1)
        tmp3 = findCow(used + 1, pos - 1)
        min = max_used
        for i in (tmp1,tmp2,tmp3):
            if i < min:
                min = i
        return min + 1
    else:
        return pos - cow

John, cow = [int(i) for i in input().split()]
max_used = abs(John - cow)
minutes = findCow(0,John)
print(minutes)
