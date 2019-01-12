while True:
    
    num_amount, m = [int(i) for i in input().strip().split()]
    if num_amount == 0 and m == 0:
        break
        
    #这段代码为什么运行错误？
    ###############################
    nums = []
    for i in range(num_amount):
        num = int(input().strip())
        nums.append(num)
    ###############################
    nums.sort()
    
    for i in range(0, num_amount, m):
        print(nums[i], end = '')
        if i < num_amount - m:
            print('', end = ' ')
    print()
   