#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sat Sep 21 20:06:57 2019
# Author: January

import sys
import is_quadratic_residue as qr_check
import find_inversion as fi
import logging

usage='''please input two integer, the first is the num needed checking and the second is the modulo.
please note that the modulo should be an odd prime, or the result can be wrong.'''

logging.basicConfig(level=logging.DEBUG)

def modPower(base, exponent, modulo):
    result = 1
    while exponent != 0:
        if exponent % 2 == 1:
            result = (result * base) % modulo
        base = (base * base) % modulo
        exponent = exponent >> 1
    return result

def extractTwos(num):
    result = num
    count = 0
    while result % 2 == 0:
        result = result >> 1
        count = count + 1
    return (count, result)


def modulo_sqrt(num, modulo):
    if (modulo - 3) % 4 == 0:
        result1 = modPower(num, int((modulo + 1) / 4), modulo)
    else:
        t, s = extractTwos(modulo - 1)
        logging.debug("t,s is (%d,%d)"%(t,s))
        for i in range(2, modulo):
            if qr_check.is_quadratic_residue(i, modulo) is False:
                logging.debug("n is %d"%(i))
                b = modPower(i, s, modulo)
                break
        result1 = modulo_sqrt_normal_prime(num, modulo, t, s, b)
    
    result2 = -result1
    while result2 < 0:
        result2 = result2 + modulo
    return (result1, result2)





def modulo_sqrt_normal_prime(a, p, t, s, b):
    ia = fi.inverse(a, p)
    logging.debug("ia is %d"%(ia))
    x = modPower(a, (s + 1) >> 1, p)
    for k in range(1, t):
        imm_v = modPower(ia * modPower(x, 2, p), 1 << (t - k), p)
        imm = modPower(ia * modPower(x, 2, p), 1 << (t - k - 1), p)
        if imm == 1:
            x = x
        elif imm == p - 1:
            x = (x * modPower(b, 1 << (k - 1), p)) % p
        else:
            logging.debug("imm:%d, imm_v:%d, error"%(imm, imm_v))
            exit(1)
    return x
        

def main():
    try:
        num = int(sys.argv[1])
        modulo = int(sys.argv[2])
    except:
        print(usage)
        exit(1)

    if qr_check.is_quadratic_residue(num, modulo) is False:
        print("No answer")
    else:
        r1, r2 = modulo_sqrt(num, modulo)
        print("the modulo square root of %d on modulo %d is %d and %d"%(num, modulo, r1, r2))
    
if __name__ == "__main__":
    main()
