from src.Lexer.lexer import lexical_analysis
from src.Syntax.parser import parser, test_parser

if __name__ == '__main__':
    lexical_analysis()
    parser()