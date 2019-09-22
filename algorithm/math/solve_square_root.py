#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Sun Sep 22 16:12:40 2019
# Author: January
import sys
import modulo_sqrt as mq
import find_inversion as fi
import logging

logger = logging.getLogger("square_root_sum_logger")
logger.setLevel(logging.DEBUG)


usage="please input a number and the number can only be 2 or in the form of 4k + 1"


# 求绝对值最小剩余
def min_abs_residue(num, modulo):
    if modulo % 2 == 1:
        limit = int((modulo - 1) / 2)
    else:
        limit = int((modulo - 2) / 2)
    residue = fi.mod(num, modulo)
    while residue > limit:
        residue = residue - modulo
    return residue


def square_sum(p):
    if p != 2 and p % 4 != 1:
        raise RuntimeError("p is invalid")
    result1 = mq.modulo_sqrt(p - 1, p)[0]
    x = result1
    y = 1
    m = int((result1 ** 2 + y) / p)
    while m > 1:
        
        u = min_abs_residue(x, m)
        v = min_abs_residue(y, m)
        logger.debug("x:%d, y:%d, u:%d, v:%d, m:%d"%(x, y, u, v, m))
        logger.debug("%d^2 + %d^2 = %d(mod p)"%(x, y, (x**2 + y**2) % p))
        x_next = int((u*x + v*y) / m)
        y_next = int((u*y - v*x) / m)
        m_next = int((x_next**2 + y_next**2) / p)
        x = x_next
        y = y_next
        m = m_next
    return (x, y)

def main():
    try:
        p = int(sys.argv[1])
    except:
        print(usage)
        exit(1)
    if p != 2 and p % 4 != 1:
        print(usage)
        exit(1)
    x, y = square_sum(p)
    print("%d^2 + %d^2 = %d"%(x, y, x**2 + y**2))

if __name__ == "__main__":
    main()
