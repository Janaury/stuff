#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Wed Sep  4 11:14:05 2019
# Author: January

import sys

def gcd_ext(big_num, small_num):
    remainder = big_num % small_num
    # print("number is %d %d"%(big_num, small_num))
    iq = int(big_num / small_num)
    if small_num % remainder == 0:
        s = 1
        t = -iq
        return (s, t)
    s_next, t_next = gcd_ext(small_num, remainder)
    # print("s t q(%d, %d, %d)"%(s_next, t_next, iq))
    s = t_next
    t = s_next - t_next * iq
    return (s, t)
    

if len(sys.argv) < 3:
    print("请传入两个数字参数")
    exit(-1)

try:
    num_big = int(sys.argv[1])
    num_small = int(sys.argv[2])
except:
    print("传入的参数非数字，请重试")

if abs(num_big) < abs(num_small):
    tmp = num_big
    num_big = num_small
    num_small = tmp

s, t = gcd_ext(num_big, num_small)
print("(s, t) is (%d, %d)"%(s, t))
