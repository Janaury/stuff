names = ('dongfangxu','zap')
case_amount = int(input())

def findMaxConsequence(name,string):
    begin = 0
    mseq = 0
    seq = 0
    while True:
        try:
            index = string.index(name, begin)
            if index == begin:
                seq = seq + 1
            else:
                if mseq < seq:
                    mseq = seq
                seq = 1
            begin = index + len(name)
        except:
            if mseq < seq:
                mseq = seq
            break
    return mseq

for index in range(case_amount):
    string = input()
    s1 = findMaxConsequence(names[0], string)
    s2 = findMaxConsequence(names[1], string)
    if s1 < s2:
        result = names[1] + '!'
    else:
        result = names[0] + '!'
    print(result)
