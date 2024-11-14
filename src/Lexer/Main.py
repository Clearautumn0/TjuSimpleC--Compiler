'''
这里可以作为独立文件运行
调用lexical_analysis_helper进行对输入数据的处理

'''

import os
import string

from src.Lexer.TransformMap import TransformMap
from src.Lexer.FA import FA
from src.Lexer.Data_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.Lexer.Helper_Func import get_closure, get_next_state, get_char_type, get_tokens
from src.Lexer.DFA import nfa_determinization
from src.Lexer.Minimize_DFA import minimize
from src.Lexer.Lexer import lexical_analysis_helper

def lexical_analysis():
    NFA = FA()
    NFA.input_symbols = lex_input_symbols
    NFA.start = lex_start
    NFA.final = lex_final
    NFA.trans_map = lex_trans_map
    NFA.state_labels = lex_state_labels

    DFA = nfa_determinization(NFA)
    min_DFA = minimize(DFA)
 
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/01_var_defn.sy", min_DFA, "1_1")
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/02_var_defn.sy", min_DFA, "1_2")
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/03_var_defn.sy", min_DFA, "1_3")
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/04_var_defn.sy", min_DFA, "1_4")
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/05_var_defn.sy", min_DFA, "1_5")
    lexical_analysis_helper("D:/000编译原理/labend/TjuSimpleC--Compiler/input/lex_input/ifelse.sy", min_DFA, "1_5")

if __name__ == "__main__":
    lexical_analysis()
