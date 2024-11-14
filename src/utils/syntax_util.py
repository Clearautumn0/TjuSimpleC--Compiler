'''
本文件是语法分析器的工具类，负责从文件中读取文法规则并解析成 Grammar 对象。
语法规则文件格式如下：

    S -> NP VP
    NP -> Det N
    VP -> V NP
    Det -> "the" | "a"
    N -> "man" | "park"
    V -> "saw" | "walked"

提供的函数有：

- load_from_file(file_path): 从文件中读取文法规则并解析成 Grammar 对象。
- 通过 grammars.get_rules()获取所有文法规则。

'''

from src.Syntax.grammar import Grammar

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

# def load_token_from_file(file_path):
# 判断字符串是否是终结符
def is_terminal(symbol, grammar:Grammar):
    non_terminals = get_non_terminal_symbols(grammar)
    return symbol not in non_terminal
            
            
if __name__ == '__main__':
    grammars = load_from_file("../../input/grammars.txt")
    print(grammars)

    for key, value in grammars.get_rules().items():
        print(key, "->", value)