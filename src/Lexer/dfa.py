'''
NFA确定化

nfa_determinization函数接受传入的NFA
返回确定化后的DFA
'''



import os
import string

from src.Lexer.TransformMap import TransformMap
from src.Lexer.FA import FA
from src.Lexer.Data_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.Lexer.helper_func import get_closure, get_next_state


def nfa_determinization(NFA):
    DFA = FA()
    processing_set = []  # 使用队列
    state_to_id = {}  # 状态集合到唯一ID的映射
    next_id = 1  # 下一个可用的状态ID

    DFA.input_symbols = NFA.input_symbols
    DFA.start = {1}
    DFA.states = {1}
    state_to_id[frozenset(get_closure(NFA.start, NFA))] = 1
    processing_set.append(frozenset(get_closure(NFA.start, NFA)))

    while processing_set:
        current_states = processing_set.pop(0)
        current_id = state_to_id[frozenset(current_states)]

        for ch in NFA.input_symbols:
            next_states = get_next_state(current_states, ch, NFA)
            if not next_states:
                continue

            if frozenset(next_states) not in state_to_id:
                next_id += 1
                state_to_id[frozenset(next_states)] = next_id
                DFA.states.add(next_id)
                processing_set.append(frozenset(next_states))
                # next_id += 1

                for state in frozenset(next_states):
                    if state in NFA.final:
                        DFA.final.add(next_id)
                        DFA.state_labels[next_id] = NFA.state_labels[state]
                        break



            DFA.trans_map.add(TransformMap(ch, current_id, state_to_id[frozenset(next_states)]))

    return DFA