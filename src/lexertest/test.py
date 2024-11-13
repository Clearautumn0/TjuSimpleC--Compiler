import os
import string


class TransformMap:
    def __init__(self, rec, now, next_):
        self.rec = rec
        self.now = now
        self.next = next_

    def __lt__(self, other):
        return self.now + 100 * ord(self.rec) < other.now + 100 * ord(self.rec)


class FA:
    def __init__(self):
        self.input_symbols = []  # 输入字符集
        self.states = set()  # 状态集合
        self.state_labels = {}  # 状态标签
        self.trans_map = set()  # 转换映射规则
        self.start = set()  # 初始状态集合
        self.final = set()  # 终态集合


# 定义符号表
symbols_table = {
    "int": "KW", 
    "void": "KW",
    "return": "KW", 
    "const": "KW", 
    "main": "KW", 
    "float": "KW", 
    "if": "KW", 
    "else": "KW",
    "+": "OP", 
    "-": "OP", 
    "*": "OP", 
    "/": "OP", 
    "%": "OP", 
    "=": "OP", 
    ">": "OP",
    "<": "OP", 
    "==": "OP", 
    "<=": "OP", 
    ">=": "OP", 
    "!=": "OP", 
    "&&": "OP", 
    "||": "OP",
    "(": "SE", 
    ")": "SE", 
    "{": "SE", 
    "}": "SE", 
    ";": "SE", 
    ",": "SE"
}

processed_symbols_table = {}

lex_input_symbols = ['n', 'l', 'o', 's', '_', '0', '=', '>', '<', '!', '&', '|', '-', '.']
lex_states = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}
lex_state_labels = {
    1: "n", 
    2: "l", 
    3: "o", 
    4: "s", 
    5: "_", 
    6: "0",
    7: "=", 
    8: ">", 
    9: "<", 
    10: "!", 
    11: "&", 
    12: "|", 
    13: "INT",
    14: "SE", 
    15: "I&K", 
    16: "OP", 
    17: "none", 
    18: "OP", 
    20: "FLOAT"
}
lex_start = {17}
lex_final = {13, 14, 15, 16, 18, 20}
lex_trans_map = {
    TransformMap('ε', 1, 13), TransformMap('n', 13, 13), TransformMap('ε', 2, 15), TransformMap('l', 15, 15),
    TransformMap('_', 15, 15), TransformMap('n', 15, 15), TransformMap('ε', 4, 14), TransformMap('ε', 3, 16),
    TransformMap('ε', 5, 15), TransformMap('ε', 7, 16), TransformMap('ε', 8, 16), TransformMap('=', 7, 16),
    TransformMap('=', 8, 16), TransformMap('ε', 9, 16), TransformMap('=', 9, 16), TransformMap('=', 10, 16),
    TransformMap('&', 11, 16), TransformMap('|', 12, 16), TransformMap('n', 18, 13), TransformMap('n', 17, 1),
    TransformMap('l', 17, 2), TransformMap('o', 17, 3), TransformMap('s', 17, 4), TransformMap('_', 17, 5),
    TransformMap('=', 17, 7), TransformMap('>', 17, 8), TransformMap('<', 17, 9), TransformMap('!', 17, 10),
    TransformMap('&', 17, 11), TransformMap('|', 17, 12), TransformMap('-', 17, 18), TransformMap('.', 13, 20),
    TransformMap('ε', 20, 20), TransformMap('n', 20, 20)
}


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
                state_to_id[frozenset(next_states)] = next_id
                DFA.states.add(next_id)
                processing_set.append(frozenset(next_states))
                next_id += 1

                if any(state in NFA.final for state in next_states):
                    DFA.final.add(next_id)
                    for state in next_states:
                        if state in NFA.final:
                            DFA.state_labels[next_id] = NFA.state_labels[state]
                            break

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

    lexical_analysis_helper("01_var_defn.sy", min_DFA, "1_1")


def lexical_analysis_helper(address, DFA, x):
    with open(address, 'r') as test_sample, open(f"./lex{x}.txt", 'w') as record_tokens:
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
        return f"<SE,{state}>"
    if label == "OP":
        return f"<OP,{state}>"
    if label == "I&K" and symbols_table.get(str_token) == "KW":
        return f"<KW,{state}>"
    return f"<IDN,{str_token}>"

  
if __name__ == "__main__":
    lexical_analysis()
