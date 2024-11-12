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
