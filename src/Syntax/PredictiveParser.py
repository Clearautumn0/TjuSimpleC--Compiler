from src.Syntax.first_and_follow import FirstAndFollow
from src.Syntax.grammar import Grammar
from src.Syntax.parsing_table import ParsingTable
from src.utils.syntax_util import get_non_terminal_symbols


class PredictiveParser:
    def __init__(self, parsing_table, non_terminals):
        self.parsing_table = parsing_table  # 解析表
        self.non_terminals = non_terminals  # 非终结符集合

    def parse(self, input_string):
        input_string += '#'  # 添加结束符号
        stack = ['#', 'E']  # 栈顶元素为结束符，栈底元素为开始符号
        # print(len(stack))
        index = 0

        steps = []
        step_number = 0

        while len(stack) > 0:
            # print(len(stack))
            top = stack[-1]  # 获取栈顶元素
            current_input = input_string[index]  # 获取当前输入字符

            if top in self.non_terminals:  # 如果栈顶元素是非终结符
                # 从解析表中查找对应的产生式
                production_rules = self.parsing_table.get((top, current_input))

                if not production_rules:  # 如果没有找到对应的产生式
                    raise SyntaxError(f"Unexpected symbol: {current_input} at position {index}")

                # 假设每个规则只有一个产生式，获取该产生式
                production = next(iter(production_rules))  # 获取字典中的第一个产生式
                # 从字典中提取产生式右部（例如 {'E': ['T', "E'"]}）
                production = production[top]

                stack.pop()  # 弹出栈顶的非终结符
                if production != ['$']:  # 如果产生式不是空串（'$'），则将产生式右部入栈
                    stack.extend(reversed(production))  # 将产生式右部反转后压入栈

                action = f"reduction"  # 当前操作为归约
                steps.append((step_number, top, current_input, action))  # 记录当前步骤
                step_number += 1
            else:  # 如果栈顶元素是终结符
                if top == current_input:  # 如果栈顶元素和当前输入匹配
                    if top == '#':  # 如果栈顶元素是结束符，则说明输入字符串已经全部匹配完毕，成功结束
                        stack.pop()  # 匹配成功，弹出栈顶元素
                        index += 1  # 移动输入指针
                        action = f"accept"  # 当前操作为接受
                        steps.append((step_number, top, current_input, action))  # 记录当前步骤
                        step_number += 1
                    else:  # 栈顶元素不是结束符，则说明匹配成功
                        stack.pop()  # 匹配成功，弹出栈顶元素
                        index += 1  # 移动输入指针
                        action = f"move"  # 当前操作为移动
                        steps.append((step_number, top, current_input, action))  # 记录当前步骤
                        step_number += 1
                else:
                    raise SyntaxError(f"Unexpected symbol: {current_input} at position {index}")

        return steps




if __name__ == '__main__':
    grammar = Grammar()

    # 添加文法规则
    grammar.add_rule("E", ["T", "E'"])
    grammar.add_rule("E'", ["+", "T", "E'"])
    grammar.add_rule("E'", ["$"])
    grammar.add_rule("T", ["F", "T'"])
    grammar.add_rule("T'", ["*", "F", "T'"])
    grammar.add_rule("T'", ["$"])
    grammar.add_rule("F", ["(", "E", ")"])
    grammar.add_rule("F", ["i"])

    # 创建解析器对象
    new_parser = FirstAndFollow(grammar, '$', "E", "#")

    first = new_parser.get_first_set()

    follow = new_parser.get_follow_set()

    t = ParsingTable(first, follow, grammar)
    M = t.build_parsing_table()

    non_terminals = get_non_terminal_symbols(grammar)
    # t.print_parsing_table()
    #
    # print("测试获取分析表中某一行的某一列的值")
    # print(t.get_production_from_table("E", "i"))

    # print(M)


    parsing_table = {}

    for A in M:
        for a in M[A]:
            tuples = (A, a)
            parsing_table[tuples] = M[A][a]
            # print(tuples, M[A][a])


    # 输入字符串
    input_string = "i*i+i"

    # 创建解析器并解析输入字符串
    parser = PredictiveParser(parsing_table, non_terminals)
    try:
        steps = parser.parse(input_string)
        for step in steps:
            print(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}")  # 打印解析步骤
    except SyntaxError as e:
        print(e)  # 输出语法错误信息
