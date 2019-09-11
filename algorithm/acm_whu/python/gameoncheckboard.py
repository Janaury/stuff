
def findMax():
    for i in range(dimen-2, -1, -1):
        for j in range(dimen):
            tmp3 = 0
            tmp2 = 0
            tmp1 = board[i+1][j]
            if j > 0:
                tmp2 = board[i+1][j-1]
            if j < dimen - 1:
                tmp3 = board[i+1][j+1]
            max = 0
            for x in (tmp1,tmp2,tmp3):
                if max < x:
                    max = x
            board[i][j] = max + board[i][j]

case_amount = int(input())

for i in range(case_amount):
    board = []
    dimen = int(input())
    for j in range(dimen):
        line = [int(x) for x in input().split()]
        board.append(line)
    findMax()
    max = 0
    for j in board[0]:
        if max < j:
            max = j
    print("Case {num}:\n{result}".format(num=i+1,result=max))
    if i != case_amount - 1:
        print()