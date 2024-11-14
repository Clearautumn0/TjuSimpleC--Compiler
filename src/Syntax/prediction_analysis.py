from grammar import Grammar
from first_and_follow import FirstAndFollow
from src.Syntax.eliminate_left_recursion import LeftRecursionEliminator
from src.Syntax.parsing_table import ParsingTable
from src.utils.syntax_util import load_from_file


# def prediction_analysis_algorithm(tokens:list, parsing_table:ParsingTable):
#     parsing_table.first_set



if __name__ == '__main__':
    test_path = "../../input/test_grammars.txt"
    path = "../../input/grammars.txt"
    ext_path = "../../input/extended_grammars.txt"
    output_path = "../../output/grammar_without_left_recursion.txt"

    old_grammar = load_from_file(test_path)
    eliminator = LeftRecursionEliminator(old_grammar)
    new_grammar = eliminator.new_productions
    # print(new_grammar)

    new_parser = FirstAndFollow(new_grammar, '$', "E", "#")
    # first = new_parser.production_first_sets
    first = {
        "E": {'(', 'i'},
        "E'": {'+', '$'},
        "T": {'(', 'i'},
        "T'": {'*', '$'},
        "F": {'(', 'i'},
        "TE'": {'(', 'i'},
        "+TE'": {'+'},
        "FT'": {'(', 'i'},
        "*FT'": {'*'},
        "(E)": {'('},
        "i": {'i'}
    }
    follow = new_parser.follow_sets
    print(follow)


    parsing_table = ParsingTable(first, follow, new_grammar.rules)
    parsing_table.print_parsing_table()
