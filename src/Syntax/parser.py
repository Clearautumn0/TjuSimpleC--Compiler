'''
语法分析器'

实现语法分析器
读入文法
读入词法分析器输出的token流，进行语法分析，生成抽象语法树。
'''
from src.Syntax.PredictiveParser import PredictiveParser
from src.Syntax.eliminate_left_recursion import LeftRecursionEliminator
from src.Syntax.first_and_follow import FirstAndFollow
from src.Syntax.parsing_table import ParsingTable
from src.utils.syntax_util import load_from_file, load_tokens, get_non_terminal_symbols, get_terminal_symbols, convert_analysis_table
from src.config import GRAMMAR_INPUT_DIR, LEX_OUTPUT_FILE

def parser():
    grammar_file_path=GRAMMAR_INPUT_DIR
    grammar = load_from_file(grammar_file_path)
    eliminator = LeftRecursionEliminator(grammar)
    grammar = eliminator.new_productions
    # print(f"消除左递归后的文法:{grammar_without_left_recursion}")

    new_parser = FirstAndFollow(grammar, '$', "program", "#")
    first_set=new_parser.get_first_set()
    follow_set=new_parser.get_follow_set()
    t = ParsingTable(first_set, follow_set, grammar)
    t.print_parsing_table()
    parsing_table = convert_analysis_table(t)


    non_terminals = get_non_terminal_symbols(grammar)
    terminals = get_terminal_symbols(grammar, "$")

    input_tokens = load_tokens(LEX_OUTPUT_FILE)
    parser = PredictiveParser(parsing_table, non_terminals, terminals)
    print("解析结果:")

    try:
        steps = parser.parse(input_tokens, "program")
        for step in steps:
            print(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}")  # 打印解析步骤
    except SyntaxError as e:
        print(e)  # 输出语法错误信息


def test_parser():
    ext_path = "../input/extended_grammars.txt"
    tokens_path = "../output/lex_output/lex1_1.txt"

    grammar = load_from_file(ext_path)

    start_token = "program"

    # 创建解析器对象
    new_parser = FirstAndFollow(grammar, '$', start_token, "#")
    first = new_parser.get_first_set()
    follow = new_parser.get_follow_set()

    t = ParsingTable(first, follow, grammar)
    M = t.build_parsing_table()

    non_terminals = get_non_terminal_symbols(grammar)
    terminals = get_terminal_symbols(grammar, "$")

    parsing_table = {}

    for A in M:
        for a in M[A]:
            tuples = (A, a)
            parsing_table[tuples] = M[A][a]

    # 输入串
    input_tokens = load_tokens(tokens_path)

    # 创建解析器并解析输入串
    parser = PredictiveParser(parsing_table, non_terminals, terminals)
    print("解析结果")
    try:
        steps = parser.parse(input_tokens, start_token)
        for step in steps:
            print(f"{step[0]}\t{step[1]}#{step[2]}\t{step[3]}")  # 打印解析步骤
    except SyntaxError as e:
        print(e)  # 输出语法错误信息


if __name__ == '__main__':
        parser()