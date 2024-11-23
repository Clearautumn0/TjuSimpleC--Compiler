"""
PredictiveParser 类实现了一个基于预测分析表的语法分析器，用于分析输入字符串是否符合给定的上下文无关文法规则。
该类封装了以下功能和函数：
1. 构造函数 (__init__)：初始化解析表、非终结符集合和终结符集合。
2. parse 函数：解析输入的 token 列表，根据预测分析表进行语法分析，输出每一步的解析操作。

类中的主要参数说明：
- parsing_table (dict): 预测分析表，键为 (非终结符, 终结符) 对，应输出产生式。
- non_terminals (list): 非终结符集合。
- terminals (list): 终结符集合。

主要函数说明：
- __init__(parsing_table, non_terminals, terminals): 初始化解析表和文法符号集合。
- parse(input_string, start_token):
  - 输入：
    - input_string (list[LexerToken]): 输入 token 列表，必须以 LexerToken 格式提供。
    - start_token (str): 文法的开始符号。
  - 输出：
    - steps (list[tuple]): 每步解析的详细信息，包括步骤编号、栈顶元素、当前输入符号及操作。
"""

from src.Syntax.first_and_follow import FirstAndFollow
from src.Syntax.parsing_table import ParsingTable
from src.utils.syntax_util import get_non_terminal_symbols, load_from_file, load_tokens, get_terminal_symbols, \
    convert_analysis_table,print_reduction_sequence
from src.Syntax.lexer_token import LexerToken


class PredictiveParser:
    """
    实现一个预测语法分析器，通过预测分析表解析输入 token 列表。
    """
    def __init__(self, parsing_table, non_terminals, terminals):
        """
        初始化 PredictiveParser 对象。
        :param parsing_table: dict, 预测分析表 (非终结符, 终结符) 对应的产生式。
        :param non_terminals: list, 文法的非终结符集合。
        :param terminals: list, 文法的终结符集合。
        """
        self.parsing_table = parsing_table  # 解析表
        self.non_terminals = non_terminals  # 非终结符集合
        self.terminals = terminals

    def parse(self, input_string: list[LexerToken], start_token: str):
        """
        使用预测分析表解析输入 token 列表。
        :param input_string: list[LexerToken], 输入的 token 列表，需以 LexerToken 格式提供。
        :param start_token: str, 文法的开始符号。
        :return: list[tuple], 包含解析步骤的详细信息，每一步为 (步骤编号, 栈顶元素, 当前输入符号, 操作)。
        """
        input_string.append(LexerToken("#", "EOF", 0))  # 添加结束符号
        stack = ['#', start_token]  # 栈顶元素为结束符，栈底元素为开始符号
        index = 0

        steps = []  # 存储解析步骤
        step_number = 0
        try:
            while len(stack) > 0:
                top = stack[-1]  # 获取栈顶元素
                current_input = input_string[index].type  # 获取当前输入字符
                if current_input not in self.terminals + self.non_terminals + ["#"]:
                    current_input = input_string[index].value

                if top in self.non_terminals:  # 如果栈顶元素是非终结符

                    # 从解析表中查找对应的产生式
                    production_rules = self.parsing_table.get((top, current_input))

                    if not production_rules:  # 如果未找到
                        print(top)
                        raise SyntaxError(f"Unexpected symbol: {current_input} at position {index} non_terminal")

                    production = next(iter(production_rules))  # 获取第一个产生式
                    production = production[top]  # 提取产生式右部

                    stack.pop()  # 弹出栈顶非终结符
                    if production != ['$']:  # 如果不是空串，将产生式右部反转后入栈
                        stack.extend(reversed(production))

                    action = "reduction"  # 当前操作为归约
                    steps.append((step_number, top, current_input, action))
                    step_number += 1

                else:  # 如果栈顶元素是终结符
                    if top == current_input:  # 如果栈顶元素和当前输入匹配
                        if top == '#' or top == "EOF":  # 如果栈顶元素是结束符，则说明输入字符串已经全部匹配完毕，成功结束
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
                        print(top)
                        raise SyntaxError(f"Unexpected symbol: {current_input} at position {index} terminal")

        except SyntaxError as e:
            # 捕获语法错误，记录当前步骤并设置错误标记
            action = "error"
            steps.append((step_number, top, current_input, action))
            print("语法错误前的规约序列：")
            for step in steps:
                print(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}")  # 输出规约序列
            print(f"语法错误: {e}")
            return steps

        return steps


if __name__ == '__main__':
    # 加载扩展文法和 token 文件路径
    ext_path = "../../input/extended_grammars.txt"
    tokens_path = "../../output/lex_output/lex1_1.txt"

    grammar = load_from_file(ext_path)
    start_token = "program"

    # 创建解析器对象并生成 FIRST 和 FOLLOW 集
    new_parser = FirstAndFollow(grammar, '$', start_token, "#")
    first = new_parser.get_first_set()
    follow = new_parser.get_follow_set()

    # 构建预测分析表
    t = ParsingTable(first, follow, grammar)
    M = t.build_parsing_table()

    non_terminals = get_non_terminal_symbols(grammar)
    terminals = get_terminal_symbols(grammar, "$")
    parsing_table = convert_analysis_table(t)

    # 加载输入串
    input_tokens = load_tokens(tokens_path)

    # 创建解析器并解析输入串
    parser = PredictiveParser(parsing_table, non_terminals, terminals)
    print("解析结果")
    try:
        steps = parser.parse(input_tokens, start_token)
        print_reduction_sequence('../../output/predictive_parser.txt',steps)
        # for step in steps:
        #     print(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}")  # 打印解析步骤
    except SyntaxError as e:
        print(e)  # 输出语法错误信息
