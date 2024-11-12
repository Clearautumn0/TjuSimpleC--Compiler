# test.py
from src.Lexer.dfa import nfa_to_dfa
from src.Lexer.lextest import MinimizedDFA
from src.Lexer.nfa import NFAGenerator
from src.Lexer.tokensAndAnalysis import Lexer

# 测试代码
code = "int main() { return 0; }"
lexer = Lexer()
tokens = lexer.tokenize(code)

print("Tokens:")
for token in tokens:
    print(f"{token[1]}: {token[0]}")

# 构建 NFA
nfa_generator = NFAGenerator(tokens)
start_state = nfa_generator.build_nfa()

print("\nNFA Transitions:")
nfa_generator.display_nfa(start_state)

# 转换为 DFA
dfa = nfa_to_dfa(start_state)
print("\nDFA Transitions:")
dfa.display_dfa()

# 最小化 DFA
minimized_dfa = MinimizedDFA(dfa)
minimized_dfa.minimize()
print("\nMinimized DFA Transitions:")
minimized_dfa.display_minimized_dfa()
