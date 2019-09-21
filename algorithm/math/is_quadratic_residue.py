#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sat Sep 21 16:45:22 2019
# Author: January

import sys
import math

usage='''please input two integer, the first is the num needed checking and the second is the modulo.
please note that the modulo should be an odd prime, or the result can be wrong.'''

def is_quadratic_residue(num, modulo):
    result = True
    if num == 1:
        return True
    if num == 2:
        imm = (modulo * modulo - 1) / 8
    elif num > 2 and num % 2 == 1:
        imm = 0
        for i in range(1, int((modulo - 1) / 2 + 1)):
            imm = (imm + int((num * i) / modulo)) % 2
    else:
        tmp = 1
        for i in range(int((modulo - 1) / 2)):
            tmp = (tmp * num) % modulo
        if tmp != 1:
            imm = 1
        else:
            imm = 2
            
    if imm % 2 == 1:
        result = False
    return result

def main():
    try:
        num = int(sys.argv[1])
        modulo = int(sys.argv[2])
    except:
        print(usage)
        exit(1)
    if (num != 2 and num % 2 != 1) or modulo % 2 != 1:
        print(usage)
        exit(1)  
    result = is_quadratic_residue(num, modulo)
    print(result)

if __name__ == "__main__":
    main()
