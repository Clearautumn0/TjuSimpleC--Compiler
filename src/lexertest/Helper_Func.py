'''
定义求闭包函数 get_closure 以及获取转移状态函数 get_next_state
get_closure:
输入：
current_states(当前状态), NFA
输出：
closure(闭包)

get_next_state:
输入：
current_states, input_, NFA
输出：
closure


'''



import os
import string

def get_closure(current_states, NFA):
    closure = set(current_states)  # 初始闭包为当前状态集合
    worklist = set(current_states)  # 工作列表，用于存储待处理的状态

    while worklist:
        state = worklist.pop()
        for tm in NFA.trans_map:
            if tm.rec == 'ε' and tm.now == state and tm.next not in closure:
                closure.add(tm.next)
                worklist.add(tm.next)

    return closure


def get_next_state(current_states, input_, NFA):
    extended_states = set()
    for state in current_states:
        for tm in NFA.trans_map:
            if tm.now == state and tm.rec == input_:
                extended_states.add(tm.next)
    return get_closure(extended_states, NFA)