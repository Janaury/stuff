# 和c语言执行结果不同？？
n = int(input())
for i in range(n):
    a,b = [int(i) for i in input().split()]
    result = (a+b)*(b-a+1)/2
    print("Case #{num}: {result}".format(num = i+ 1, result= int(result)))