#Tokens 处理
#输出结果为tokens序列，每一个序列项是 【value，类型】这样的小组合


import re

# 定义词法单元类型和关键词、运算符、界符
KEYWORDS = ["int", "float", "char", "void", "return", "const", "main"]
OPERATORS = ["!", "+", "-", "*", "/", "%", "=", ">", "<", "==", "<=", ">=", "!=", "&&", "||"]
SEPARATORS = ["(", ")", "{", "}", ";", ","]
TOKEN_TYPES = {
    "KW": "关键字",
    "IDN": "标识符",
    "OP": "运算符",
    "SE": "界符",
    "INT": "整数",
    "FLOAT": "浮点数",
    "CHAR": "单字符",
    "STRING": "字符串"
}

# 词法分析器
class Lexer:
    def __init__(self):
        self.tokens = []
        self.current_index = 0

    def tokenize(self, code):
        patterns = {
            "KW": r"\b(?:int|float|char|void|return|const|main)\b",
            "IDN": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            "OP": r"[!+\-*/%=><&|=]+",
            "SE": r"[(){},;]",
            "INT": r"\b\d+\b",
            "FLOAT": r"\b\d+\.\d+\b",
            "CHAR": r"'.?'",
            "STRING": r'"[^"]*"'
        }

        token_regex = "|".join(f"(?P<{type}>{pattern})" for type, pattern in patterns.items())
        for match in re.finditer(token_regex, code):
            type = match.lastgroup
            value = match.group(type)
            self.tokens.append((value, TOKEN_TYPES[type]))
        return self.tokens

    def next_token(self):
        if self.current_index < len(self.tokens):
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        return None
