#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Sep  3 12:01:38 2019
# Author: January
import math
import sys

# 读取范围值
if len(sys.argv) > 1:
    try:
        max = int(sys.argv[1])
    except:
        print("argument is not a valid integer ")
        exit(-1)
else:
    while True:
        try:
            max = int(input("please input the upper bound of search range(>=2):"))
            break
        except:
            print("not a integer, try again")


prime = [True for i in range(max + 1)]
# 0和1不在计算范围内
prime[0] = False
prime[1] = False

for i in range(2, int(math.sqrt(max) + 1)):
    if prime[i] == True:
        j = i + i
        for j in range(i+i, max + 1, i):
            prime[j] = False
            j = j + i
    # 当prime[i]执行结束时，要保证算法的正确，必须保证prime[i+1]的内容是正确的
    # 根据定理，在prime[i]执行结束时，小于等于i^2的prime数组内容都是正确的，由于i >= 2, i^2 >= i + 1
    # 该算法正确

# 打印结果
for i in range(2, max + 1):
    if prime[i]:
        print(i, end=' ')

print()
