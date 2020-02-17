#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Mon Feb 17 13:05:43 2020
# Author: January

import sys

usage='''transform binary file to c char array
ex_c_char <filename>"
'''
def main():
    if len(sys.argv) < 2:
        print(usage)
        
    filename = sys.argv[1]
    with open(sys.argv[1], "rb") as f:
        data = f.read()
        print("{", end = "")
        for item in data:
            print("0x%02x"%(item), end = ",")
        print("\b}")
    
if __name__ == "__main__":
    main()
