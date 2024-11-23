"""
    本文件是 FIRST 和 FOLLOW 集合计算器的类。
    该类用于计算上下文无关文法（CFG）的 FIRST 集合和 FOLLOW 集合。

    该类提供了以下方法：

    - `__init__(self, grammar, space_symbol, start_symbol, end_symbol)`: 构造函数，用于初始化类实例。
      初始化时会计算文法的 FIRST 集合和 FOLLOW 集合，以及产生式的 FIRST 集合。

    - `compute_non_terminals(self, grammar)`: 计算非终结符集合。
      遍历文法的产生式规则，找出所有的非终结符。

    - `compute_terminals(self, grammar, space_symbol)`: 计算终结符集合。
      遍历文法的产生式规则，找出所有的终结符。

    - `compute_first(self, grammar, space_symbol)`: 计算 FIRST 集合。
      对文法进行递归计算，得出每个非终结符的 FIRST 集合。

    - `compute_follow(self, grammar, first_sets, space_symbol, start_symbol, end_symbol)`: 计算 FOLLOW 集合。
      通过递归计算 FOLLOW 集合，根据 FIRST 集合的计算结果推导 FOLLOW 集合。

    - `compute_production_first(self, grammar, space_symbol)`: 计算产生式的 FIRST 集合。
      通过遍历每个产生式，计算出其 FIRST 集合。

    - `merge_dicts(self, dict1, dict2)`: 合并两个字典。
      将两个字典的内容合并为一个字典。

    参数说明：

    - `grammar`: `Grammar` 类的实例，包含文法的产生式规则。
    - `space_symbol`: 空串符号，通常用 'ε' 表示。
    - `start_symbol`: 文法的开始符号。
    - `end_symbol`: 结束符号，通常用 '#' 表示，用于表示输入结束。

    返回值说明：

    - `first_sets`: 字典，包含每个非终结符的 FIRST 集合。
    - `follow_sets`: 字典，包含每个非终结符的 FOLLOW 集合。
    - `production_first_sets`: 字典，包含每个产生式的 FIRST 集合。

    @author: <聂哲浩>
"""
from grammar import Grammar
from src.utils.syntax_util import get_non_terminal_symbols, get_terminal_symbols


class FirstAndFollow:
    def __init__(self, grammar, space_symbol, start_symbol, end_symbol):
        self.grammar = grammar.rules  # 文法规则
        self.terminals = get_terminal_symbols(grammar, space_symbol)  # 计算终结符
        self.non_terminals = get_non_terminal_symbols(grammar)  # 计算非终结符
        self.first_sets = self.compute_first(grammar, space_symbol)  # 计算 FIRST 集
        self.follow_sets = self.compute_follow(grammar, self.first_sets, space_symbol, start_symbol, end_symbol)  # 计算 FOLLOW 集
        self.production_first_sets = self.compute_production_first(grammar, space_symbol)  # 计算产生式的 FIRST 集
        self.first_all=merge_dicts(self.first_sets,self.production_first_sets) #合并FIRST集和产生式的FIRST集
    def get_first_set(self):
        return self.first_all
    def get_follow_set(self):
        return self.follow_sets

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
                    if all(symbol == space_symbol for symbol in production):  # 如果产生式为 $
                        if space_symbol not in first_sets[non_terminal]:
                            first_sets[non_terminal].add(space_symbol)
                            changed = True

        return first_sets

    # 计算产生式的 FIRST 集
    def compute_production_first(self, grammar, space_symbol):
        production_first_sets = {}

        for non_terminal, productions in grammar.rules.items():
            for production in productions:
                if len(production) == 1:
                    production_tuple = (production[0])  # 仅有一个元素时，显式地加上逗号
                else:
                    production_tuple = tuple(production)

                production_first_sets[production_tuple] = set()

                # 处理空串
                if space_symbol in production:
                    production_first_sets[production_tuple].add(space_symbol)
                    continue

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
                    # 如果遇到空串 $
                    elif symbol == space_symbol:
                        # if space_symbol not in production_first_sets[production_tuple]:
                        #     production_first_sets[production_tuple].add(space_symbol)
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


def merge_dicts(dict1, dict2):
    """合并两个字典"""
    merged_dict = dict1.copy()  # 先复制第一个字典
    merged_dict.update(dict2)    # 更新为第二个字典的内容
    return merged_dict




# 测试
if __name__ == '__main__':
    # 创建文法对象
    grammar = Grammar()

    # 添加文法规则
    grammar.add_rule("E", ["T", "E'"])
    grammar.add_rule("E'", ["+", "T", "E'"])
    grammar.add_rule("E'", ["$"])
    grammar.add_rule("E'", ["$"])
    grammar.add_rule("T", ["F", "T'"])
    grammar.add_rule("T'", ["*", "F", "T'"])
    grammar.add_rule("T'", ["$"])
    grammar.add_rule("T'", ["$"])
    grammar.add_rule("F", ["(", "E", ")"])
    grammar.add_rule("F", ["i"])

    # 创建解析器对象
    new_parser = FirstAndFollow(grammar, '$', "E", "#")
    new_parser = FirstAndFollow(grammar, '$', "E", "#")

    # 输出解析结果
    print("Non-terminals:", new_parser.grammar.keys())  # 输出非终结符
    print("Terminals:", new_parser.terminals)  # 输出终结符
    print("Productions:", new_parser.grammar.values())  # 输出产生式规则
    print("FIRST sets:", new_parser.first_sets)  # 输出 FIRST 集合
    print("FOLLOW sets:", new_parser.follow_sets)  # 输出 FOLLOW 集合
    print("Production FIRST sets:", new_parser.production_first_sets)  # 输出产生式的 FIRST 集合

    for production, first_set in new_parser.production_first_sets.items():
        print(production, ":", first_set)    # 输出每个产生式的 FIRST 集

