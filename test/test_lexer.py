# test.py
from src.Lexer.dfa import nfa_to_dfa
from src.Lexer.lextest import MinimizedDFA
from src.Lexer.nfa import NFAGenerator
from src.Lexer.Lex import Lexer

# 测试代码
# code = "int main() { return 0; }"
input_filepath = r'D:\000编译原理\labend\TjuSimpleC--Compiler\input\lexer.txt'
output_filepath = r'D:\000编译原理\labend\TjuSimpleC--Compiler\output\lexer_output.txt'

with open(input_filepath, 'r', encoding='utf-8') as file:
    code = file.read()


lexer = Lexer()
tokens = lexer.tokenize(code)

with open(output_filepath, 'w', encoding='utf-8') as file:
    file.write("Tokens:\n")
    for token in tokens:
        file.write(f"{token[1]}: {token[0]} \n")

# 构建 NFA
nfa_generator = NFAGenerator(tokens)
start_state = nfa_generator.build_nfa()

# print("\nNFA Transitions:")
nfa_generator.display_nfa(start_state)

# 转换为 DFA
dfa = nfa_to_dfa(start_state)
# print("\nDFA Transitions:")
dfa.display_dfa()

# 最小化 DFA
minimized_dfa = MinimizedDFA(dfa)
minimized_dfa.minimize()
# print("\nMinimized DFA Transitions:")
minimized_dfa.display_minimized_dfa()
