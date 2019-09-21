#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Wed Sep  4 11:14:05 2019
# Author: January

import sys

# a_1 = q_1*a_2 + a_3 ---> a_3 = a_1 - q*a_2

# a_{n-3} = q_{n-3}*a_{n-2} + a_{n-1} ---> a_{n-1} = a_{n-3} - q_{n-3}*a_{n-2}
# a_{n-2} = q_{n-2}*a_{n-1} + a_n ---> a_n = a_{n-2} - q_{n-2}*a_{n-1} 
#我们需要将a_{n-2}和a_{n-1}逐步替换到a_1和a_2, 得到最后结果a_n = s*a_1 + t*a_2
# a_{n-1} = q_{n-1} * a_n ---> a_n为最大公因数
#
# 下面推导递推关系
# 我们设 a_n = s_{n-2}*a_{n-2} + t_{n-2}*a_{n-1} ----------- 式1
# 下一步需要求出 a_n = s_{n-3}*a_{n-3} + t_{n-3}*a_{n-2}中的s_{n-3}和t_{n-3}
# 我们将 a_{n-1} = a_{n-3} - q_{n-3}*a_{n-2}带入式1，得到 a_n = t_{n-2}*a_{n-3} + {s_{n-2}-t_{n-2}*q_{n-3}}*a{n-2}
# 因此可以得到递推关系s_{n-3} = t_{n-2}, t_{n-3} = s_{n-2}-t_{n-2}*q_{n-3}
# 按照这个递推关系，可以求出s_1和t_1即为所求
 



def gcd_ext(big_num, small_num):
    remainder = big_num % small_num
    # print("number is %d %d"%{big_num, small_num))
    iq = int(big_num / small_num)
    if small_num % remainder == 0:
        s = remainder
        t = -iq
        return (s, t, remainder)
    s_next, t_next, gcd = gcd_ext(small_num, remainder)
    # print("s t q(%d, %d, %d)"%(s_next, t_next, iq))
    s = t_next
    t = s_next - t_next * iq
    return (s, t, gcd)
    

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

s, t, gcd = gcd_ext(num_big, num_small)
print("%d * %d + %d * %d = %d"%(s, num_big, t, num_small, gcd))
