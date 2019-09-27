#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Date: Fri Sep 27 21:14:50 2019
# Author: January
# state:
# (ml, sl, b)
# action:
# (1,1,1)
# (1,0,1)
# (0,1,1)
# (0,2,1)
# (2,0,1)



import numpy as np

actions = np.array(((1,1,1),
                    (1,0,1),
                    (0,1,1),
                    (0,2,1),
                    (2,0,1)))

def findPath(state, action):
    state_n = state + action
    if state.min() < 0 and state[0] < state[1]:
        return False
    
        
    

def main():
    
    
if __name__ == "__main__":
    main()
