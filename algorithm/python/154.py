case = 0
while True:
    p = input()
    if p == '#':
        break
    case = case + 1
    string = ""
    for i in range(len(p)):
        if i % 2 == 1:
            string = string + p[i].upper()
        else:
            string = string + p[i]
    print("Case {num}: {s}".format(num=case ,s=string))
