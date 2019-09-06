#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Wed Sep  4 10:48:54 2019
# Author: January

import sys

def gcd(big_num, small_num):
    remainder = big_num % small_num
    if remainder == 0:
        return small_num
    return gcd(small_num, remainder)
    

if len(sys.argv) < 3:
    print("请传入两个数字参数")
    exit(-1)

try:
    num_big = int(sys.argv[1])
    num_small = int(sys.argv[2])
except:
    print("传入的参数非数字，请重试")

if num_big < num_small:
    tmp = num_big
    num_big = num_small
    num_small = tmp

result = gcd(num_big, num_small)
print("the greatest common factor of %d and %d is %d"%(num_big, num_small, result))
