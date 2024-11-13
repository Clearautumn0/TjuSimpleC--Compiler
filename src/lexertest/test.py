import os
import string

from src.lexertest.TransformMap import TransformMap
from src.lexertest.FA import FA
from src.lexertest.Date_Deal import symbols_table, symbols, processed_symbols_table, lex_input_symbols, lex_start, lex_final, lex_state_labels, lex_states, lex_trans_map
from src.lexertest.Helper_Func import get_closure, get_next_state


# def get_closure(current_states, NFA):
#     closure = set(current_states)  # 初始闭包为当前状态集合
#     worklist = set(current_states)  # 工作列表，用于存储待处理的状态

#     while worklist:
#         state = worklist.pop()
#         for tm in NFA.trans_map:
#             if tm.rec == 'ε' and tm.now == state and tm.next not in closure:
#                 closure.add(tm.next)
#                 worklist.add(tm.next)

#     return closure


# def get_next_state(current_states, input_, NFA):
#     extended_states = set()
#     for state in current_states:
#         for tm in NFA.trans_map:
#             if tm.now == state and tm.rec == input_:
#                 extended_states.add(tm.next)
#     return get_closure(extended_states, NFA)


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


                # if any(state in NFA.final for state in next_states):
                #     DFA.final.add(next_id)
                #     for state in next_states:
                #         if state in NFA.final:
                #             DFA.state_labels[next_id] = NFA.state_labels[state]
                #             break

            DFA.trans_map.add(TransformMap(ch, current_id, state_to_id[frozenset(next_states)]))

    return DFA


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
                if ch not in string.whitespace:  # 忽略空白字符
                    ch_type = get_char_type(ch)  # 获取当前字符的类型
                    matched = False  # 标记是否有匹配的状态转移
                    for tm in DFA.trans_map:
                        if current_state == tm.now and ch_type == tm.rec:
                            current_state = tm.next
                            str_token += ch  # 将字符加到当前的 token 中
                            matched = True
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

  
if __name__ == "__main__":
    lexical_analysis()
