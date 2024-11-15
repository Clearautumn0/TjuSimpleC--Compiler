'''
本文件是语法分析器的工具类，
load_from_file() 函数负责从文件中读取文法规则并解析成 Grammar 对象。
语法规则文件格式如下：

    S -> NP VP
    NP -> Det N
    VP -> V NP
    Det -> "the" | "a"
    N -> "man" | "park"
    V -> "saw" | "walked"

load_tokens() 函数负责从文件中读取 token，返回 Token 实例的列表。
token 文件格式如下：
void    <KW, 4>
func    <IDN, func>
(    <SE, 23>
)    <SE, 24>
{    <SE, 25>

本工具集中提供的函数有：

- load_tokens(filename): 从文件中读取 token，返回 Token 实例的列表。
- load_from_file(file_path): 从文件中读取文法规则并解析成 Grammar 对象。
- 通过 grammars.get_rules()获取所有文法规则。
- 通过 grammars.get_non_terminal_symbols()获取所有非终结符。
- 通过 grammars.get_terminal_symbols()获取所有终结符。
- 通过 is_terminal(symbol, grammar)判断符号是否是终结符。




@Author1: <覃邱维>
@Author2: <王俊哲>

'''

from src.Syntax.grammar import Grammar
from src.Syntax.lexer_token import LexerToken


# 加载tokens文件
def load_tokens(filename):
    """从文件中读取 token，返回 Token 实例的列表"""
    tokens = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()  # 去除行首尾的空白字符
            if line:  # 确保行不为空
                # 按空格拆分，取第一个部分为类型，第二个部分为值和ID
                type_part, value_id_part = line.split(' <')
                value, token_id = value_id_part[:-1].split(',')  # 去掉尾部的 > 并拆分
                token_id = token_id.strip()  # 清理可能的空白字符
                token = LexerToken(type_part.strip(), value.strip(), token_id.strip())
                tokens.append(token)

    return tokens

# 加载文法
def load_from_file(file_path):
    grammar = Grammar()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # 忽略空行和注释行
            
            # 将文法规则分割为左侧和右侧
            lhs, rhs = line.split("->")
            lhs = lhs.strip()  # 去掉空格
            rhs_options = [r.strip() for r in rhs.split('|')]
            
            # 添加文法规则到 Grammar 中
            for rhs in rhs_options:
                # 直接用 rhs 包含分号
                grammar.add_rule(lhs, rhs.strip().split())
    return grammar

# 获取非终结符
def get_non_terminal_symbols(grammar:Grammar):
    # 非终结符集合
    return list(grammar.get_rules().keys())

# 获取终结符
def get_terminal_symbols(grammar:Grammar, space_symbol:str):
    non_terminals = get_non_terminal_symbols(grammar)
    terminals = set()
    # 遍历文法规则，识别终结符
    for lhs, productions in grammar.rules.items():
        for production in productions:
            for symbol in production:
                if symbol not in non_terminals:  # 如果符号不是非终结符，说明它是终结符
                    terminals.add(symbol)
    terminals.add(space_symbol)  # 添加空串符号
    return list(terminals)

# 判断字符串是否是终结符
def is_terminal(symbol, grammar:Grammar):
    non_terminals = get_non_terminal_symbols(grammar)
    return symbol not in non_terminals

# 转换分析表形式
def convert_analysis_table(parsing_table):
    M = parsing_table.get_parsing_table()
    result_table = {}
    for A in M:
        for a in M[A]:
            tuples = (A, a)
            result_table[tuples] = M[A][a]
    return result_table

# 打印规约序列
def print_reduction_sequence(file_path, steps):
    with open(file_path, 'w', encoding='utf-8') as file:
        for step in steps:
            file.write(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}\n")# 打印解析步骤


            
if __name__ == '__main__':
    # grammars = load_from_file("../../input/grammars.txt")
    # print(grammars)
    #
    # for key, value in grammars.get_rules().items():
    #     print(key, "->", value)


    tokens_path="../../output/lex_output/lex1_1.txt"
    tokens = load_tokens(tokens_path)
    print(tokens[1].type)
    print(tokens[1].value)
    print(tokens[1].id)
    print("测试token加载：")
    for token in tokens:
        print(token)