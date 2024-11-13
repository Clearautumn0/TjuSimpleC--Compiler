from grammar import Grammar


class FirstAndFollow:
    def __init__(self, grammar, space_symbol, start_symbol, end_symbol):
        self.grammar = grammar.rules  # 文法规则
        self.terminals = self.compute_terminals(grammar, space_symbol)  # 计算终结符
        self.non_terminals = self.compute_non_terminals(grammar)  # 计算非终结符
        self.first_sets = self.compute_first(grammar, space_symbol)  # 计算 FIRST 集
        self.follow_sets = self.compute_follow(grammar, self.first_sets, space_symbol, start_symbol, end_symbol)  # 计算 FOLLOW 集
        self.production_first_sets = self.compute_production_first(grammar, space_symbol)  # 计算产生式的 FIRST 集

    # 计算非终结符
    def compute_non_terminals(self, grammar):
        return set(grammar.rules.keys())  # 返回文法中的非终结符集合

    # 计算终结符
    def compute_terminals(self, grammar, space_symbol):
        non_terminals = set(grammar.rules.keys())
        terminals = set()

        # 遍历文法规则，识别终结符
        for lhs, productions in grammar.rules.items():
            for production in productions:
                for symbol in production:
                    if symbol not in non_terminals:  # 如果符号不是非终结符，说明它是终结符
                        terminals.add(symbol)

        terminals.add(space_symbol)  # 添加空串符号
        return terminals

    # 计算 FIRST 集
    def compute_first(self, grammar, space_symbol):
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
                            break  # 只处理第一个符号
                        elif symbol in first_sets:  # 如果是非终结符
                            if space_symbol not in first_sets[symbol]:
                                for char in first_sets[symbol]:
                                    if char != space_symbol and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)
                                        changed = True
                                break  # 只处理第一个非终结符
                            else:  # 如果包含空串
                                for char in first_sets[symbol]:
                                    if char != space_symbol and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)
                                        changed = True
                                if index == len(production) - 1:
                                    if space_symbol not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(space_symbol)
                                        changed = True
                                continue  # 继续查看下一个符号
                    if all(symbol == space_symbol for symbol in production):  # 如果产生式为 ε
                        if space_symbol not in first_sets[non_terminal]:
                            first_sets[non_terminal].add(space_symbol)
                            changed = True

        return first_sets

    # 计算产生式的 FIRST 集
    def compute_production_first(self, grammar, space_symbol):
        production_first_sets = {}

        for non_terminal, productions in grammar.rules.items():
            for production in productions:
                # 使用元组表示产生式的右部
                production_tuple = tuple(production)

                # 计算右边符号序列的 FIRST 集
                production_first_sets[production_tuple] = set()

                for index, symbol in enumerate(production):
                    # 如果是终结符，直接将其加入产生式 FIRST 集
                    if symbol in self.terminals:
                        production_first_sets[production_tuple].add(symbol)
                        break
                    # 如果是非终结符，加入其 FIRST 集
                    elif symbol in self.non_terminals:
                        production_first_sets[production_tuple].update(self.first_sets[symbol])
                        # 如果 FIRST 集中有空串，继续向下推导
                        if space_symbol in self.first_sets[symbol]:
                            continue
                        else:
                            break
                    # 如果遇到空串 ε
                    elif symbol == space_symbol:
                        if space_symbol not in production_first_sets[production_tuple]:
                            production_first_sets[production_tuple].add(space_symbol)
                        break

        return production_first_sets

    # 计算 FOLLOW 集
    def compute_follow(self, grammar, first_sets, space_symbol, start_symbol, end_symbol):
        follow_sets = {non_terminal: set() for non_terminal in grammar.rules.keys()}
        follow_sets[start_symbol].add(end_symbol)  # 开始符号的 FOLLOW 集包含 EOF

        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.rules.items():
                for production in productions:
                    for i, current_symbol in enumerate(production):
                        if current_symbol in self.non_terminals:
                            follow_to_add = set()

                            for j in range(i + 1, len(production)):
                                next_symbol = production[j]
                                if next_symbol in self.terminals:
                                    follow_to_add.add(next_symbol)
                                    break
                                if next_symbol in first_sets:
                                    follow_to_add.update(first_sets[next_symbol] - {space_symbol})

                                if space_symbol in first_sets.get(next_symbol, set()):
                                    continue
                                else:
                                    break

                            if i == len(production) - 1 or all(
                                    symbol in self.non_terminals and space_symbol in first_sets.get(symbol, set())
                                    for symbol in production[i + 1:]
                            ):
                                follow_to_add.update(follow_sets[non_terminal])

                            if follow_to_add - follow_sets[current_symbol]:
                                follow_sets[current_symbol].update(follow_to_add)
                                changed = True

        return follow_sets


# 测试
if __name__ == '__main__':
    # 创建文法对象
    grammar = Grammar()

    # 添加文法规则
    grammar.add_rule("E", ["T", "E'"])
    grammar.add_rule("E'", ["+", "T", "E'"])
    grammar.add_rule("E'", ["ε"])
    grammar.add_rule("T", ["F", "T'"])
    grammar.add_rule("T'", ["*", "F", "T'"])
    grammar.add_rule("T'", ["ε"])
    grammar.add_rule("F", ["(", "E", ")"])
    grammar.add_rule("F", ["i"])

    # 创建解析器对象
    new_parser = FirstAndFollow(grammar, 'ε', "E", "#")

    # 输出解析结果
    print("Non-terminals:", new_parser.grammar.keys())  # 输出非终结符
    print("Terminals:", new_parser.terminals)  # 输出终结符
    print("Productions:", new_parser.grammar.values())  # 输出产生式规则
    print("FIRST sets:", new_parser.first_sets)  # 输出 FIRST 集合
    print("FOLLOW sets:", new_parser.follow_sets)  # 输出 FOLLOW 集合
    print("Production FIRST sets:", new_parser.production_first_sets)  # 输出产生式的 FIRST 集合

    for production, first_set in new_parser.production_first_sets.items():
        print(production, ":", first_set)    # 输出每个产生式的 FIRST 集

