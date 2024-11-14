'''
定义求闭包函数 get_closure、获取转移状态函数 get_next_state、获取读取字符类型函数get_char_type、获取tokens函数get_tokens
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


get_char_type:
输入：
读取的字符ch
输出：
ch对应的的类型


get_tokens:
输入：
当前状态state、当前的识别到的token、DFA
输出：
token对应的输出格式

'''



import os
import string

from src.Lexer.Data_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map

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


def get_char_type(ch):
    if ch.isdigit():
        return 'n'
    if ch == '.':
        return '.'
    if ch.isalpha():
        return 'l'
    if ch in "+-*/%":
        return 'o'
    if ch in "();{},":
        return 's'
    return ch


def get_tokens(state, str_token, DFA):
    label = DFA.state_labels.get(state, "")
    if label == "INT":
        return f"<INT,{str_token}>"
    if label == "FLOAT":
        return f"<FLOAT,{str_token}>"
    if label == "SE":
        return f"<SE,{symbols.get(str_token)}>"
    if label == "OP":
        return f"<OP,{state}>"
    if label == "I&K" and symbols_table.get(str_token) == "KW":
        return f"<KW,{symbols.get(str_token)}>"
    return f"<IDN,{str_token}>"