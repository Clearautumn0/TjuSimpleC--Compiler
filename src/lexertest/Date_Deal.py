from src.lexertest.TransformMap import TransformMap
from src.lexertest.FA import FA

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

# 定义字符映射表
symbols = {
    "int": 1,
    "float": 2,
    "char": 3,
    "void": 4,
    "return": 5,
    "const": 6,
    "main": 7,
    # 运算符 OP
    "!": 8,
    "+": 9,
    "-": 10,
    "*": 11,
    "/": 12,
    "%": 13,
    "=": 14,
    ">": 15,
    "<": 16,
    "==": 17,
    "<=": 18,
    ">=": 19,
    "!=": 20,
    "&&": 21,
    "||": 22    ,
    # 界符 SE
    "(": 23,
    ")": 24,
    "{": 25,
    "}": 26,
    ";": 27,
    ",": 28
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
