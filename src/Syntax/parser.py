class Grammar:
    def __init__(self):
        self.rules = {}

    def add_rule(self, non_terminal, production):
        if non_terminal not in self.rules:
            self.rules[non_terminal] = []
        self.rules[non_terminal].append(production)


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar.rules
        self.terminals = self.compute_terminals(grammar)
        self.non_terminals = self.compute_non_terminals(grammar)
        self.first_sets = self.compute_first(grammar)
        self.follow_sets = self.compute_follow(grammar, self.first_sets, 'compUnit')

    # 计算非终结符
    def compute_non_terminals(self, grammar):
        return set(grammar.rules.keys())

    # 计算终结符
    def compute_terminals(self, grammar):
        non_terminals = set(grammar.rules.keys())
        terminals = set()

        for lhs, productions in grammar.rules.items():
            for production in productions:
                for symbol in production:
                    if symbol not in non_terminals:
                        terminals.add(symbol)

        terminals.add('$')  # 添加 EOF 符号
        return terminals

    # 计算 FIRST 集
    def compute_first(self, grammar):
        first_sets = {non_terminal: set() for non_terminal in grammar.rules.keys()}

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.rules.items():
                for production in productions:
                    for index, symbol in enumerate(production):
                        if symbol in self.terminals:  # 如果是终结符
                            if symbol not in first_sets[non_terminal]:
                                first_sets[non_terminal].add(symbol)
                                changed = True
                            break  # 只处理第一个终结符或非终结符
                        elif symbol in first_sets:  # 如果是非终结符
                            if '$' not in first_sets[symbol]:
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
                                if index == len(production) - 1:
                                    if '$' not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add('$')
                                        changed = True
                                continue  # 继续查看下一个符号
                    if all(symbol == '$' for symbol in production):
                        if '$' not in first_sets[non_terminal]:
                            first_sets[non_terminal].add('$')
                            changed = True

        return first_sets

    # 计算 FOLLOW 集
    def compute_follow(self, grammar, first_sets, start_symbol):
        follow_sets = {non_terminal: set() for non_terminal in grammar.rules.keys()}
        follow_sets[start_symbol].add('#')  # 开始符号的 FOLLOW 集合包含 EOF

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.rules.items():
                for production in productions:
                    for i in range(len(production) - 1):
                        current_symbol = production[i]
                        next_symbol = production[i + 1]

                        # 1. 当前符号是非终结符，且下一个符号是非终结符
                        if current_symbol in self.non_terminals and next_symbol in self.non_terminals:
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
    grammar = Grammar()
    grammar.add_rule("compUnit", ["decl", "compUnit"])
    grammar.add_rule("compUnit", ["funcDef", "compUnit"])
    grammar.add_rule("compUnit", ["$"])
    grammar.add_rule("decl", ["typeSpec", "varDeclList", ";"])
    grammar.add_rule("typeSpec", ["int"])
    grammar.add_rule("varDeclList", ["varDecl", ",", "varDeclList"])
    grammar.add_rule("varDeclList", ["varDecl"])
    grammar.add_rule("varDecl", ["id", "[", "num", "]", "=", "num"])
    grammar.add_rule("varDecl", ["id", "=", "num"])
    grammar.add_rule("funcDef", ["typeSpec", "id", "(", "params", ")", "{", "compUnit", "}"])
    grammar.add_rule("params", ["param", ",", "params"])

    new_parser = Parser(grammar)
    print("Non-terminals:", new_parser.grammar.keys())
    print("Productions:", new_parser.grammar.values())
    print("Terminals:", new_parser.terminals)
    print("FIRST sets:", new_parser.first_sets)
    print("FOLLOW sets:", new_parser.follow_sets)
