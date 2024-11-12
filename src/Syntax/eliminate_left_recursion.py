from unittest.mock import right

from grammar import Grammar


class LeftRecursionEliminator:
    def __init__(self, old_productions:Grammar):
        self.old_productions = old_productions
        self.non_terminal_symbols, terminal_symbols = self.get_symbols(self.old_productions)
        self.eliminate_left_recursion(self.non_terminal_symbols, self.old_productions)

    # 获取非终结符与终结符集合
    def get_symbols(self, old_productions:Grammar):
        # 非终结符集合
        non_terminal_symbols = []
        for lhs in old_productions.rules.keys():
            non_terminal_symbols.append(lhs)
        # 终结符集合
        terminal_symbols = set()
        for rhs_list in old_productions.rules.values():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol not in non_terminal_symbols and symbol != "$":
                        terminal_symbols.add(symbol)
        return non_terminal_symbols, list(terminal_symbols)

    # 消除左递归
    def eliminate_left_recursion(self, non_terminal_symbols:list, productions:Grammar):
        new_productions = productions
        for i in range(len(non_terminal_symbols)):
            for j in range(i):
                i_mark = non_terminal_symbols[i]
                j_mark = non_terminal_symbols[j]
                i_rules = new_productions.rules[i_mark]
                j_rules = new_productions.rules[j_mark]
                new_productions.rules[i_mark] = self.expand_grammar(i_rules, j_rules, j_mark)
            self.eliminate_direct_left_recursion_for_one_rule(new_productions.rules[non_terminal_symbols[i]])
        print(new_productions)

    # 实现带入
    def expand_grammar(self, i_rules, j_rules, j_mark):
        # 创建新的 program 规则列表
        new_program_rules = []
        for target_rule in i_rules:
            for source_rule in j_rules:
                new_rule = []
                for t in target_rule:
                    if t != j_mark:
                        new_rule.append(t)
                    else:
                        for s in source_rule:
                            new_rule.append(s)
                if new_rule != ['$']:
                    while '$' in new_rule:
                        new_rule.remove('$')
                new_program_rules.append(new_rule)
        return new_program_rules

    # 消除直接左递归
    def eliminate_direct_left_recursion_for_one_rule(self, lhs, rhs):
        left_recursive = [token for l in rhs if lhs == rhs[0]]
        non_left_recursive = [prod for prod in rule if prod[0] != rule[0][0]]
        if not left_recursive:
            return rule

        new_rules = non_left_recursive
        new_rules.append([right for right in left_recursive[0]])




# 测试
if __name__ == "__main__":
    oldGrammar = Grammar()

    oldGrammar.rules = {
        'compUnit': [['decl', 'compUnit'], ['funcDef', 'compUnit'], ['$']],
        'program': [['compUnit', 'a']]

    }

    newGrammar = LeftRecursionEliminator(oldGrammar)
