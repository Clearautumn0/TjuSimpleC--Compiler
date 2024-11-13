'''
符号表定义
'''
from src.new_lexer.transform_map import TransformMap

symbols_table = {
    "int": "KW", "void": "KW", "return": "KW", "const": "KW",
    "main": "KW", "float": "KW", "if": "KW", "else": "KW",
    "+": "OP", "-": "OP", "*": "OP", "/": "OP", "%": "OP",
    "=": "OP", ">": "OP", "<": "OP", "==": "OP", "<=": "OP",
    ">=": "OP", "!=": "OP", "&&": "OP", "||": "OP",
    "(": "SE", ")": "SE", "{": "SE", "}": "SE", ";": "SE", ",": "SE"
}

# 记录已经处理过的符号及其类别，类似符号表的映射
processed_symbols_table = {}

# 存储所有需要在词法分析中处理的符号
lex_input_symbols = ['n', 'l', 'o', 's', '_', '0', '=', '>', '<', '!', '&', '|', '-', '.']

# 状态集合，包含所有词法分析过程中的状态
lex_states = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20}

# 状态标签可以通过一个字典来表示，其中键是状态，值是标签
lex_state_labels = {
    1: "n", 2: "l", 3: "o", 4: "s", 5: "_", 7: "=",
    8: ">", 9: "<", 10: "!", 11: "&", 12: "|", 13: "INT",
    14: "SE", 15: "I&K", 16: "OP", 17: "none", 18: "OP",
    20: "FLOAT"
}

# 起始状态和终态
lex_start = {17}  # 假设 17 是起始状态

lex_final = {13, 14, 15, 16, 18, 20}


# 定义转换规则集合
lex_trans_map = {
    TransformMap('ε', 1, 13), TransformMap('n', 13, 13), TransformMap('ε', 2, 15),
    TransformMap('l', 15, 15), TransformMap('_', 15, 15), TransformMap('n', 15, 15),
    TransformMap('ε', 4, 14), TransformMap('ε', 3, 16), TransformMap('ε', 5, 15),
    TransformMap('ε', 7, 16), TransformMap('ε', 8, 16), TransformMap('=', 7, 16),
    TransformMap('=', 8, 16), TransformMap('ε', 9, 16), TransformMap('=', 9, 16),
    TransformMap('=', 10, 16), TransformMap('&', 11, 16), TransformMap('|', 12, 16),
    TransformMap('n', 18, 13), TransformMap('n', 17, 1), TransformMap('l', 17, 2),
    TransformMap('o', 17, 3), TransformMap('s', 17, 4), TransformMap('_', 17, 5),
    TransformMap('=', 17, 7), TransformMap('>', 17, 8), TransformMap('<', 17, 9),
    TransformMap('!', 17, 10), TransformMap('&', 17, 11), TransformMap('|', 17, 12),
    TransformMap('-', 17, 18), TransformMap('.', 13, 20), TransformMap('ε', 20, 20),
    TransformMap('n', 20, 20)
}

# 字符识别函数
def get_char_type(ch, next_ch):
    if '0' <= ch <= '9':  # 判断数字字符
        return 'n'
    if ch == '.':  # 判断小数点
        return '.'
    if ('A' <= ch <= 'Z') or ('a' <= ch <= 'z'):  # 判断字母字符
        return 'l'
    if ch in ['+', '-', '*', '/', '%']:  # 判断运算符
        return 'o'
    if ch in ['(', ')', '{', '}', ';', ',']:  # 判断分隔符
        return 's'
    # 如果是小数点，但下一个字符不是数字，则抛出错误
    if ch == '.' and (not ('0' <= next_ch <= '9')):
        raise ValueError("浮点数输入错误")
    return ch  # 返回原字符（如果不属于上述任何类型）

# 生成符号表
def generate_symbol_table(state, str_token, DFA):
    # 根据状态标签和符号表更新符号表
    state_label = DFA.state_labels[state]
    
    # 如果符号是 INT, SE, 或 OP 并且没有处理过
    if state_label in ["INT", "SE", "OP"] and str_token not in processed_symbols_table:
        processed_symbols_table.add(str_token)
        # 可以根据需求将符号加入到符号表中
        symbols_table[str_token] = state_label
        
    # 处理 "I&K" 和关键字 KW 的情况
    elif state_label == "I&K" and symbols_table.get(str_token) == "KW" and "KW" not in processed_symbols_table:
        processed_symbols_table.add(str_token)
        symbols_table[str_token] = state_label

    # 如果符号没有出现在已处理的符号表中，则将其视为标识符 "IDN"
    elif str_token not in processed_symbols_table:
        processed_symbols_table.add(str_token)
        symbols_table[str_token] = "IDN"



def get_tokens(state, str_token, DFA):
    # 获取当前符号的 token 字符串表示
    state_label = DFA.lex_state_labels[state]
    
    if state_label == "INT":
        return f"<INT,{str_token}>"
    if state_label == "FLOAT":
        return f"<FLOAT,{str_token}>"
    if state_label == "SE":
        return f"<SE,{state}>"
    if state_label == "OP":
        return f"<OP,{state}>"
    if state_label == "I&K" and symbols_table.get(str_token) == "KW":
        return f"<KW,{state}>"
    
    # 如果是标识符
    return f"<IDN,{str_token}>"