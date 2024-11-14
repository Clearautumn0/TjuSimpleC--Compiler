'''
lexical_analysis_helper实现了对输入代码的读取和分析并在此过程中调用get_tokens获取输出的tokens序列

'''

import os
import string

from src.Lexer.TransformMap import TransformMap
from src.Lexer.FA import FA
from src.Lexer.Data_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.Lexer.Helper_Func import get_closure, get_next_state, get_char_type, get_tokens
from src.Lexer.DFA import nfa_determinization
from src.Lexer.Minimize_DFA import minimize


def lexical_analysis_helper(address, DFA, x):
    output_dir = "D:/000编译原理/labend/TjuSimpleC--Compiler/output/lex_output"
    output_filename = f"lex{x}.txt"
    output_path = os.path.join(output_dir, output_filename)
    with open(address, 'r') as test_sample, open(output_path, 'w') as record_tokens:
        if not test_sample or not record_tokens:
            print("文件打开失败")
            return

        current_state = next(iter(DFA.start))  # 初始状态
        str_token = ""
        for line in test_sample:
            i = 0  # 初始化索引
            while i < len(line):
                ch = line[i]  # 当前字符
                print(f"+ {ch} +")
                if ch not in string.whitespace:  # 忽略空白字符
                    ch_type = get_char_type(ch)  # 获取当前字符的类型
                    # print(f"--{ch_type}--")
                    matched = False  # 标记是否有匹配的状态转移
                    # print(DFA.trans_map)
                    for tm in DFA.trans_map:
                        # print(f"{current_state} + {tm.now} + {tm.rec}")
                        if current_state == tm.now and ch_type == tm.rec:
                            current_state = tm.next
                            str_token += ch  # 将字符加到当前的 token 中
                            matched = True
                            # print(f"+ {current_state} + {str_token} + ")
                            break
                    
                    if matched:  # 如果找到了匹配的状态转移
                        # 检查当前状态是否是接受状态，并查看下一个字符
                        if current_state in DFA.final:
                            # 如果当前字符不是终结状态，继续检查下一个字符
                            next_state = None
                            if i + 1 < len(line):  # 如果不是最后一个字符
                                next_ch = line[i + 1]
                                next_ch_type = get_char_type(next_ch)
                                for tm_next in DFA.trans_map:
                                    if current_state == tm_next.now and next_ch_type == tm_next.rec:
                                        next_state = tm_next.next
                                        break
                            
                            if not next_state or next_state not in DFA.final:
                                # 如果没有找到继续匹配的状态，或者下一个状态不是终结状态
                                record_tokens.write(f"{str_token} {get_tokens(current_state, str_token, DFA)}\n")
                                str_token = ""  # 重置当前 token
                                current_state = next(iter(DFA.start))  # 回到初始状态
                    # 无匹配的情况，跳过当前字符
                i += 1  # 移动到下一个字符
