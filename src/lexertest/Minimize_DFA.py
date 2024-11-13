'''
DFA最小化
传入DFA, 返回最小化后的DFA

'''

import os
import string

from src.lexertest.TransformMap import TransformMap
from src.lexertest.FA import FA
from src.lexertest.Date_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.lexertest.Helper_Func import get_closure, get_next_state
from src.lexertest.DFA import nfa_determinization


def minimize(DFA):
    min_DFA = FA()
    state_mapping = {}
    non_final_states = set()
    final_states_by_label = set()

    for state in DFA.states:
        if state in DFA.final:
            final_states_by_label.add(state)
        else:
            non_final_states.add(state)

    new_state_id = 0
    for state in non_final_states:
        state_mapping[state] = new_state_id
        new_state_id += 1
    for state in final_states_by_label:
        state_mapping[state] = new_state_id
        new_state_id += 1

    for old_state, new_state in state_mapping.items():
        min_DFA.states.add(new_state)
        if old_state in DFA.start:
            min_DFA.start.add(new_state)
        if old_state in DFA.final:
            min_DFA.final.add(new_state)
            min_DFA.state_labels[new_state] = DFA.state_labels[old_state]

    for tm in DFA.trans_map:
        new_now = state_mapping[tm.now]
        new_next = state_mapping[tm.next]
        min_DFA.trans_map.add(TransformMap(tm.rec, new_now, new_next))

    return min_DFA
