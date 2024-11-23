'''
这里可以作为独立文件运行
调用lexical_analysis_helper进行对输入数据的处理

'''

import os
import string

from src.Lexer.TransformMap import TransformMap
from src.Lexer.FA import FA
from src.Lexer.Data_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.Lexer.helper_func import get_closure, get_next_state, get_char_type, get_tokens
from src.Lexer.dfa import nfa_determinization
from src.Lexer.minimize_dfa import minimize
from src.utils.lexer_util import lexical_analysis_helper

def lexical_analysis():
    # print('++\n++')
    NFA = FA()
    NFA.input_symbols = lex_input_symbols
    NFA.start = lex_start
    NFA.final = lex_final
    NFA.trans_map = lex_trans_map
    NFA.state_labels = lex_state_labels

    DFA = nfa_determinization(NFA)
    min_DFA = minimize(DFA)
 

    lexical_analysis_helper( min_DFA)


if __name__ == "__main__":
    lexical_analysis()
