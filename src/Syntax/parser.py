

from grammar import Grammar

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.terminals = self.compute_terminals(grammar)
        self.non_terminals = self.compute_non_terminals(grammar)
        self.first_sets = self.compute_first(grammar)
        self.follow_sets = self.compute_follow(grammar, self.first_sets, 'program')


    # 计算非终结符
    def compute_non_terminals(self, grammar):
        return set(grammar.keys())

    # 计算终结符
    def compute_terminals(self, grammar):
        # 获取所有非终结符的集合
        non_terminals = set(grammar.keys())

        # 获取所有终结符的集合
        terminals = set()
        for lhs, productions in grammar.items():  # lhs 是非终结符，productions 是产生式列表
            for production in productions:
                for symbol in production:  # 遍历产生式右侧的每个符号
                    if symbol not in non_terminals:
                        terminals.add(symbol)
        terminals.add('$')  # 添加 EOF 符号
        return terminals

    # 计算 FIRST 集
    def compute_first(self, grammar):
        # 初始化 FIRST 集合，存储每个非终结符的 FIRST 集合
        first_sets = {non_terminal: set() for non_terminal in grammar.keys()}

        changed = True  # 用来标记 FIRST 集合是否有变化
        while changed:
            changed = False
            # 遍历每个非终结符
            for non_terminal, productions in grammar.items():
                for production in productions:
                    # print(production)
                    # print(non_terminal,first_sets[non_terminal])
                    # 遍历产生式的每个符号
                    for index, symbol in enumerate(production):
                        if symbol in self.terminals:  # 如果是终结符
                            # 直接将终结符添加到 FIRST 集合中
                            if symbol not in first_sets[non_terminal]:
                                first_sets[non_terminal].add(symbol)
                                changed = True
                            break  # 只处理第一个终结符或非终结符
                        elif symbol in first_sets:  # 如果是非终结符
                            # 如果 FIRST 集合没有空串，则停止
                            if '$' not in first_sets[symbol]:
                                # 将 FIRST(symbol) 中的所有符号（排除 $）添加到 FIRST(non_terminal)
                                for char in first_sets[symbol]:
                                    if char != '$' and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)
                                        changed = True
                                break  # 只处理第一个非终结符
                            else:  # 如果包含空串，则继续添加 FIRST 集合的内容
                                for char in first_sets[symbol]:
                                    if char != '$' and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)
                                        changed = True
                                # 如果是最后一个符号，则考虑空串
                                if index == len(production) - 1:
                                    if '$' not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add('$')
                                        changed = True
                                continue  # 继续查看下一个符号
                    # 如果产生式完全推导出空串，也要考虑空串（$）
                    if all(symbol == '$' for symbol in production):
                        if '$' not in first_sets[non_terminal]:
                            first_sets[non_terminal].add('$')
                            changed = True

        return first_sets

    # 计算 FOLLOW 集
    def compute_follow(self, grammar, first_sets, start_symbol):
        # 初始化 FOLLOW 集合
        follow_sets = {non_terminal: set() for non_terminal in grammar.keys()}
        follow_sets[start_symbol].add('#')  # 开始符号的 FOLLOW 集合包含 EOF

        # 迭代直到所有 FOLLOW 集合稳定
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.items():
                for production in productions:
                    for i in range(len(production) - 1):
                        current_symbol = production[i]
                        next_symbol = production[i + 1]
                        print(current_symbol, next_symbol)

                        # 1. 当前符号是非终结符，且下一个符号是非终结符
                        if current_symbol in self.non_terminals and next_symbol in self.non_terminals:
                            # 将 next_symbol 的 FIRST 集合（去除空串）加入到 current_symbol 的 FOLLOW 集合中
                            new_elements = first_sets[next_symbol] - {'$'}
                            if new_elements - follow_sets[current_symbol]:
                                follow_sets[current_symbol].update(new_elements)
                                changed = True

                        # 2. 当前符号是非终结符，且下一个符号是终结符
                        elif current_symbol in self.non_terminals and next_symbol in self.terminals:
                            if next_symbol not in follow_sets[current_symbol]:
                                follow_sets[current_symbol].add(next_symbol)
                                changed = True

                    # 3. 处理产生式右侧最后一个符号是非终结符的情况
                    if production[-1] in self.non_terminals:
                        new_elements = follow_sets[non_terminal] - follow_sets[production[-1]]
                        if new_elements:
                            follow_sets[production[-1]].update(new_elements)
                            changed = True

        return follow_sets

# 测试
if __name__ == '__main__':
    test_grammar = {
        'compUnit': [['decl', 'compUnit'], ['funcDef', 'compUnit'], ['$']],
        'program': [['compUnit', 'a']]
    }

    new_parser = Parser(test_grammar)
    print("Non-terminals:", new_parser.grammar.keys())
    print("Productions:", new_parser.grammar.values())
    print("Terminals:", new_parser.terminals)
    print("FIRST sets:", new_parser.first_sets)
    print("FOLLOW sets:", new_parser.follow_sets)
