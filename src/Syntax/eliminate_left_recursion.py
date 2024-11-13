from grammar import Grammar
from src.utils.syntax_util import load_from_file


class LeftRecursionEliminator:
    def __init__(self, old_productions:Grammar):
        self.old_productions = old_productions
        self.new_productions = self.old_productions
        self.non_terminal_symbols = []
        self.terminal_symbols = []
        self.start_symbol = None
        self.get_symbols()
        self.eliminate_left_recursion()

    # 获取非终结符与终结符集合
    def get_symbols(self):
        # 非终结符集合
        non_terminal_symbols = []
        for lhs in self.old_productions.get_rules().keys():
            non_terminal_symbols.append(lhs)
        # 终结符集合
        terminal_symbols = set()
        for rhs_list in self.old_productions.get_rules().values():
            for rhs in rhs_list:
                for symbol in rhs:
                    if symbol not in non_terminal_symbols and symbol != "$":
                        terminal_symbols.add(symbol)
        self.non_terminal_symbols = non_terminal_symbols
        self.start_symbol = self.non_terminal_symbols[0]
        self.terminal_symbols = list(terminal_symbols)

    # 消除左递归
    def eliminate_left_recursion(self):
        for i in range(len(self.non_terminal_symbols)):
            i_mark = self.non_terminal_symbols[i]
            for j in range(i):
                j_mark = self.non_terminal_symbols[j]
                i_rules = self.new_productions.rules[i_mark]
                j_rules = self.new_productions.rules[j_mark]
                self.new_productions.rules[i_mark] = self.expand_grammar(i_mark, i_rules, j_mark, j_rules)
            # print(self.new_productions.rules)
            self.eliminate_direct_left_recursion_for_one_rule(i_mark, self.new_productions.rules[i_mark])
        self.remove_useless_productions()
        # print(self.new_productions)

    # 实现规则改写
    def expand_grammar(self, i_mark:str, i_rules:list, j_mark:str, j_rules:list):
        # 创建新的 program 规则列表
        new_rules = set()
        for target_rule in i_rules:
            # j能由i推导出
            if j_mark == target_rule[0]:
                for source_rule in j_rules:
                    new_rule = []
                    new_rule.extend(source_rule)
                    new_rule.extend(target_rule[1:])

                    if new_rule != ['$']:
                        while '$' in new_rule:
                            new_rule.remove('$')
                    # print(new_rules)
                    new_rules.add(tuple(new_rule))
            else:
                new_rules.add(tuple(target_rule))
        # print(new_rules)
        # print('---------------')
        res_list = [list(r) for r in new_rules]

        return res_list

    # 消除直接左递归
    def eliminate_direct_left_recursion_for_one_rule(self, lhs:str, rhs_rules:list[list]):
        left_recursive = []
        non_left_recursive = []
        for rhs in rhs_rules:
            if rhs[0] == lhs:
                left_recursive.append(rhs[1:])
            else:
                non_left_recursive.append(rhs)

        if not left_recursive:
            return rhs_rules

        new_lhs = f"{lhs}'"
        # 将非左递归产生式添加新的非终结符
        for nlr in non_left_recursive:
            nlr.append(new_lhs)
        # 将左递归产生式（去掉左递归部分）添加新的非终结符
        for lr in left_recursive:
            lr.append(new_lhs)
        left_recursive.append(['$'])

        self.new_productions.rules[lhs] = non_left_recursive
        self.new_productions.rules[new_lhs] = left_recursive

    # 删除无用产生式
    def remove_useless_productions(self):
        non_terminals = set(self.non_terminal_symbols)
        reachable = {symbol: False for symbol in non_terminals}
        reachable[self.start_symbol] = True
        pre_cond = {}
        cur_cond = reachable
        while cur_cond != pre_cond:
            pre_cond = dict(cur_cond)
            for symbol, is_reachable in reachable.items():
                if is_reachable:
                    for prod in self.new_productions.rules[symbol]:
                        for token in prod:
                            if token in reachable.keys():
                                reachable[token] = True
            cur_cond = reachable
        for k, v in reachable.items():
            if not v:
                del self.new_productions.rules[k]




# 测试
if __name__ == "__main__":
    test_path = "../../input/test_grammars.txt"
    path = "../../input/grammars.txt"
    oldGrammar = load_from_file(path)
    newGrammar = LeftRecursionEliminator(oldGrammar)
    print(newGrammar.new_productions)
