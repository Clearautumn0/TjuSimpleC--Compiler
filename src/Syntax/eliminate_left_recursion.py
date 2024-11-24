from grammar import Grammar
from src.utils.syntax_util import load_from_file, get_non_terminal_symbols, get_terminal_symbols, remove_duplicates


class LeftRecursionEliminator:
    """
    消除左递归，传入Grammar类对象
    eliminate_left_recursion(non_terminal_symbols, grammar): 传入非终结符list，Grammar类对象，返回去除左递归的Grammar对象
    """
    def __init__(self, old_productions:Grammar):
        self.old_productions = old_productions
        self.new_productions = self.old_productions
        self.non_terminal_symbols = get_non_terminal_symbols(self.new_productions)
        self.terminal_symbols = get_terminal_symbols(self.new_productions, "$")
        self.new_productions = self.eliminate_left_recursion(self.non_terminal_symbols, self.new_productions)

    # 消除左递归
    def eliminate_left_recursion(self, non_terminal_symbols:list, grammar:Grammar):
        """
        :param non_terminal_symbols: 非终结符列表
        :param grammar: Grammar对象
        :return: 消除左递归后的Grammar对象
        """
        for i in range(len(non_terminal_symbols)):
            i_mark = non_terminal_symbols[i]
            for j in range(i):
                j_mark = non_terminal_symbols[j]
                i_rules = grammar.rules[i_mark]
                j_rules = grammar.rules[j_mark]
                grammar.rules[i_mark] = self.__expand_grammar(i_mark, i_rules, j_mark, j_rules)
            self.__eliminate_direct_left_recursion_for_one_rule(i_mark, grammar.rules[i_mark])
        self.__remove_useless_productions(non_terminal_symbols, grammar)
        return grammar

    # 实现规则改写
    def __expand_grammar(self, i_mark:str, i_rules:list, j_mark:str, j_rules:list):
        # 创建新的 program 规则列表
        new_rules = []
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
                    new_rules.append(tuple(new_rule))
            else:
                new_rules.append(tuple(target_rule))

        remove_duplicates(new_rules)
        res_list = [list(r) for r in new_rules]
        return res_list

    # 消除直接左递归
    def __eliminate_direct_left_recursion_for_one_rule(self, lhs:str, rhs_rules:list[list]):
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
    def __remove_useless_productions(self, non_terminal_symbols:list, new_productions:Grammar):
        non_terminals = non_terminal_symbols
        reachable = {symbol: False for symbol in non_terminals}
        reachable[non_terminal_symbols[0]] = True
        pre_cond = {}
        cur_cond = reachable
        while cur_cond != pre_cond:
            pre_cond = dict(cur_cond)
            for symbol, is_reachable in reachable.items():
                if is_reachable:
                    for prod in new_productions.rules[symbol]:
                        for token in prod:
                            if token in reachable.keys():
                                reachable[token] = True
            cur_cond = reachable
        for k, v in reachable.items():
            if not v:
                del new_productions.rules[k]
        return new_productions


# 测试
if __name__ == "__main__":
    pass
