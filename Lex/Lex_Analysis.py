import os
import re

# 关键字、运算符和界符的定义
keywords = {
    'int': '<KW,1>',
    'float': '<KW,2>',
    'char': '<KW,3>',
    'void': '<KW,4>',
    'return': '<KW,5>',
    'const': '<KW,6>',
    'main': '<KW,7>',
}

operators = {
    '!': '<OP,1>',
    '+': '<OP,2>',
    '-': '<OP,3>',
    '*': '<OP,4>',
    '/': '<OP,5>',
    '%': '<OP,6>',
    '=': '<OP,7>',
    '>': '<OP,8>',
    '<': '<OP,9>',
    '==': '<OP,10>',
    '<=': '<OP,11>',
    '>=': '<OP,12>',
    '!=': '<OP,13>',
    '&&': '<OP,14>',
    '||': '<OP,15>',
}

separators = {
    '(': '<SE,1>',
    ')': '<SE,2>',
    '{': '<SE,3>',
    '}': '<SE,4>',
    ';': '<SE,5>',
    ',': '<SE,6>',
}

# 正则表达式模式
patterns = {
    'IDN': r'^[a-zA-Z_][a-zA-Z0-9_]*',
    'INT': r'^\d+',
    'FLOAT': r'^\d+\.\d+',
    'CHAR': r"^'.'",
    'STR': r'^"[^"]*"',
}

# 符号表
symbol_table = {}

# 词法分析函数
def lexer(file_path):
    with open(file_path, 'r') as file:
        code = file.read()  # 读取文件内容

    code = code.splitlines()  # 按行分割代码
    tokens = []

    for line in code:
        line = line.strip()  # 去除行首尾空白
        while line:
            line = line.lstrip()  # 去掉开头空白
            # 匹配关键字
            for keyword in keywords:
                if line.lower().startswith(keyword):  # 不区分大小写
                    tokens.append(f"{keyword} {keywords[keyword]}")
                    line = line[len(keyword):].lstrip()
                    if keyword.lower() not in symbol_table:
                        symbol_table[keyword.lower()] = keywords[keyword]
                    break
            else:
                # 匹配运算符
                for operator in operators:
                    if line.startswith(operator):
                        tokens.append(f"{operator} {operators[operator]}")
                        line = line[len(operator):].lstrip()
                        break
                else:
                    # 匹配界符
                    for separator in separators:
                        if line.startswith(separator):
                            tokens.append(f"{separator} {separators[separator]}")
                            line = line[len(separator):].lstrip()
                            break
                    else:
                        # 匹配标识符、整数、浮点数、字符、字符串
                        matched = False
                        for token_type, pattern in patterns.items():
                            match = re.match(pattern, line)
                            if match:
                                token_value = match.group()
                                tokens.append(f"{token_value} <{token_type}, {token_value}>")
                                line = line[match.end():].lstrip()
                                # if token_type == 'IDN':
                                #     # 添加标识符到符号表
                                #     if token_value not in symbol_table:
                                #         symbol_table[token_value] = '<IDN>'
                                matched = True
                                break
                        if not matched:
                            print(f"Error: Unrecognized token in line: {line}")
                            break

    return tokens

# 写入tokens到文件
def write_tokens_to_file(tokens, output_file_path):
    with open(output_file_path, 'w') as output_file:
        for token in tokens:
            output_file.write(token + '\n')

# 测试代码
if __name__ == "__main__":
    # 获取 test_data 目录下的所有 txt 文件
    directory = "../test_data"
    output_directory = "../output_data"  # 输出文件夹路径
    os.makedirs(output_directory, exist_ok=True)  # 创建输出文件夹（如果不存在）

    for filename in os.listdir(directory):
        if filename.endswith(".txt") and filename.startswith("test"):
            file_path = os.path.join(directory, filename)
            print(f"Reading tokens from: {file_path}")
            tokens = lexer(file_path)

            # 生成输出文件路径
            output_file_path = os.path.join(output_directory, f"{filename}_tokens.txt")
            write_tokens_to_file(tokens, output_file_path)
            print(f"Tokens written to: {output_file_path}")

