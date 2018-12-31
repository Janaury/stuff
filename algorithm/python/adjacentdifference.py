def getdiff(num_list):
    last = 0
    result = []
    for num in num_list:
        result.append(num - last)
        last = num
    result.sort()
    result = [str(i) for i in result]
    return ' '.join(result)
    
case_amount = int(input())
for i in range(case_amount):
    num_amount = int(input())
    nums = [int(i) for i in input().split()]
    print("Case {serial}:\n{seq}".format(serial=i+1,seq=getdiff(nums)))
    if i != case_amount - 1:
        print()
