#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Sep  3 21:22:48 2019
# Author: January
import sys

stack = []
NUMBER_TABLE = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
USAGE='第一个参数为需要转换的10进制数字，第二个参数为进制，默认是2'
stack = []

num_system = 2
if len(sys.argv) <= 1:
    print(USAGE)
    exit(-1)
else:
    try:
        decimal_num = int(sys.argv[1])
    except:
        print("参数非数字")
        exit(-1)
    if len(sys.argv) > 2:
        try:
            num_system = int(sys.argv[2])
            if num_system > 16:
                print('进制需要小于等于16')
                exit(-1)
        except:
            print("参数非数字")
            exit(-1)

q = decimal_num
r = 0
while q != 0:
    r = q % num_system
    q = int(q / num_system)
    stack.append(r)

print("num_system is %d"%(num_system))
print("result is ", end='')

if num_system <= 10:
    for i in range(len(stack) - 1, -1, -1):
        print(stack[i], end='')
else:
    for i in range(len(stack) - 1, -1, -1):
        print(NUMBER_TABLE[stack[i]], end='')
print()