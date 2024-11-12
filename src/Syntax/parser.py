from grammar import Grammar


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar.rules  # 文法规则
        self.terminals = self.compute_terminals(grammar)  # 计算终结符
        self.non_terminals = self.compute_non_terminals(grammar)  # 计算非终结符
        self.first_sets = self.compute_first(grammar)  # 计算 FIRST 集
        self.follow_sets = self.compute_follow(grammar, self.first_sets, 'compUnit')  # 计算 FOLLOW 集

    # 计算非终结符
    def compute_non_terminals(self, grammar):
        # 非终结符即文法规则中的左侧部分
        return set(grammar.rules.keys())

    # 计算终结符
    def compute_terminals(self, grammar):
        # 获取文法中的所有非终结符
        non_terminals = set(grammar.rules.keys())
        terminals = set()

        # 遍历文法规则，识别终结符
        for lhs, productions in grammar.rules.items():
            for production in productions:
                for symbol in production:
                    # 如果该符号不是非终结符，则它是终结符
                    if symbol not in non_terminals:
                        terminals.add(symbol)

        terminals.add('$')  # 添加 EOF 符号（表示输入的结束）
        return terminals

    # 计算 FIRST 集
    def compute_first(self, grammar):
        # 初始化非终结符的 FIRST 集
        first_sets = {non_terminal: set() for non_terminal in grammar.rules.keys()}

        # 用来标记 FIRST 集是否有改变
        changed = True
        while changed:
            changed = False
            for non_terminal, productions in grammar.rules.items():
                for production in productions:
                    for index, symbol in enumerate(production):
                        if symbol in self.terminals:  # 如果是终结符
                            if symbol not in first_sets[non_terminal]:
                                first_sets[non_terminal].add(symbol)  # 将终结符加入 FIRST 集
                                changed = True
                            break  # 只处理第一个终结符或非终结符
                        elif symbol in first_sets:  # 如果是非终结符
                            if '$' not in first_sets[symbol]:  # 如果 FIRST 集不包含空串
                                for char in first_sets[symbol]:
                                    if char != '$' and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)  # 将 FIRST 集加入当前非终结符的 FIRST 集
                                        changed = True
                                break  # 只处理第一个非终结符
                            else:  # 如果包含空串，则继续添加 FIRST 集合的内容
                                for char in first_sets[symbol]:
                                    if char != '$' and char not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add(char)  # 将 FIRST 集加入当前非终结符的 FIRST 集
                                        changed = True
                                if index == len(production) - 1:  # 如果是生产式最后一个符号
                                    if '$' not in first_sets[non_terminal]:
                                        first_sets[non_terminal].add('$')  # 如果能推导空串，添加空串
                                        changed = True
                                continue  # 继续查看下一个符号
                    if all(symbol == '$' for symbol in production):  # 如果整个产生式是空串
                        if '$' not in first_sets[non_terminal]:
                            first_sets[non_terminal].add('$')  # 添加空串
                            changed = True

        return first_sets

    # 计算 FOLLOW 集
    def compute_follow(self, grammar, first_sets, start_symbol):
        # 初始化非终结符的 FOLLOW 集
        follow_sets = {non_terminal: set() for non_terminal in grammar.rules.keys()}
        follow_sets[start_symbol].add('#')  # 开始符号的 FOLLOW 集合包含 EOF（#）

        # 用来标记 FOLLOW 集是否有改变
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
                            # 将 next_symbol 的 FIRST 集（去除空串）加入到 current_symbol 的 FOLLOW 集合中
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
                        # 将 FOLLOW(non_terminal) 中的所有元素加入到 production[-1] 的 FOLLOW 集合中
                        if follow_sets[non_terminal] - follow_sets[production[-1]]:
                            follow_sets[production[-1]].update(follow_sets[non_terminal])
                            changed = True

        return follow_sets


# 测试
if __name__ == '__main__':
    # 创建文法对象
    grammar = Grammar()

    # 添加文法规则
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

    # 创建解析器对象
    new_parser = Parser(grammar)

    # 输出解析结果
    print("Non-terminals:", new_parser.grammar.keys())  # 输出非终结符
    print("Terminals:", new_parser.terminals)  # 输出终结符
    print("Productions:", new_parser.grammar.values())  # 输出产生式规则
    print("FIRST sets:", new_parser.first_sets)  # 输出 FIRST 集合
    print("FOLLOW sets:", new_parser.follow_sets)  # 输出 FOLLOW 集合
