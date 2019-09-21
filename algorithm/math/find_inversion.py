#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sat Sep 21 09:31:55 2019
# Author: January
import sys

def mod(num, modulo):
    while num < 0:
        num = num + modulo
    num = num % modulo
    return num

def gcd_ext(big_num, small_num, modulo):
    iq = int(big_num / small_num)
    residue = big_num % small_num
    if small_num % residue == 0:
        s = residue
        t = mod(-iq, modulo)
        return (s, t, residue)
    s_next, t_next, gcd = gcd_ext(small_num, residue, modulo)
    s = t_next
    t = mod(s_next - iq * t_next, modulo)
    return (s, t, gcd)
# 不同模互质的数是否就一定没有逆元呢？
def inverse(num, modulo):
    if num > modulo:
        num = mod(num, modulo)
    s, t, gcd = gcd_ext(modulo, num, modulo)
    if gcd != 1:
        return 0
    else:
        return t
 
def main():
    if len(sys.argv) < 3:
        print("please input two positive integers, the first is the number needed inversing and the second is the modulo")
        exit(1)
    try:
        a = int(sys.argv[1])
        modulo = int(sys.argv[2])
    except:
        print("输入的不是合法正整数，请输入两个数字, 按照需要求逆的数，模的顺序排列")
        print("invalid integer, please try again")
        exit(1)
    if a <= 0 or modulo <= 0:
        print("the numbers you input are not positive, please try again")
        exit(0)
    
    ia = get_inverse(a, modulo)
    print("the iversion of %d on %d modulo is %d"%(a, modulo, ia))
    # print("%d*%d=%d"%(a, ia, mod(a*ia, modulo)))

if __name__ == "__main__":
    main()
    
