#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Tue Sep  3 11:23:00 2019
# Author: January
import math
import sys

def check_prime(num, primes):
    is_prime = True
    test_upper = int(math.sqrt(num))
    for prime in primes:
        if prime > test_upper:
            break
        else:
            if num % prime == 0:
                is_prime = False
                break
    return is_prime

def main():
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
    result = []
    if max < 2:
        print("no prime")
    else:
        for i in range(2, max + 1):
            if check_prime(i, result):
                result.append(i)
        print(result)

if __name__ == "__main__":
    main()

    





