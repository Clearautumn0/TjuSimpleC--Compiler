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
from src.utils.syntax_util import load_from_file, load_tokens, get_non_terminal_symbols, get_terminal_symbols, convert_analysis_table,print_reduction_sequence,visualize_parsing_table
from src.config import GRAMMAR_INPUT_DIR, LEX_OUTPUT_FILE, PARSER_OUTPUT_FILE, VISUALIZE_PARSING_TABLE


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
    # t.print_parsing_table()
    parsing_table = convert_analysis_table(t)
    # 可视化解析表
    if VISUALIZE_PARSING_TABLE:
        visualize_parsing_table(t.get_parsing_table())

    non_terminals = get_non_terminal_symbols(grammar)
    terminals = get_terminal_symbols(grammar, "$")

    input_tokens = load_tokens(LEX_OUTPUT_FILE)
    parser = PredictiveParser(parsing_table, non_terminals, terminals)
    print("解析结果:")

    parser_output_file_path = PARSER_OUTPUT_FILE
    try:
        steps = parser.parse(input_tokens, "program")
        print_reduction_sequence(parser_output_file_path, steps)
    except SyntaxError as e:
        print(e)  # 输出语法错误信息

if __name__ == '__main__':
        parser()