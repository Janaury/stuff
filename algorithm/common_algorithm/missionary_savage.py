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

path = []
viewed_states = set()

def isValidState(state):
    missionary, savage, boat = state
    if missionary < 0 or savage < 0 or boat < 0:
        return False
    if missionary > 3 or savage > 3 or boat > 1:
        return False

    # 左岸被吃
    if missionary < savage and missionary != 0:
        return False
    
    # 右岸被吃
    if missionary > savage and missionary != 3:
        return False
    
    return True


def findPath(state):
    valid = False
    if isValidState(state) is False:
        return False
    
    # 找到路径了
    state_tuple = tuple(state)
    if state_tuple == (3,3,1) :
        return True
    # 已经搜索过这个状态，进入循环
    if state_tuple in viewed_states :
        return False
    
    viewed_states.add(state_tuple)
    # 继续寻找
    for action in np.vstack((actions, -actions)):
        valid = findPath(state + action)
        if valid is True:
            path.append(action)
            break
    # 从该节点回溯，删除对该节点范围记录
    viewed_states.remove(state_tuple)
    return valid


def main():
    init = np.array((0,0,0))
    result = findPath(init)
    if result is False:
        print("no route")

    state = init
    print("init state:" + str(state))
    for i in range(len(path)-1, -1, -1):
        state += path[i]
        print('action:'+ str(path[i]) + ' ' + 'state:' + str(state))
            
            
    
if __name__ == "__main__":
    main()
