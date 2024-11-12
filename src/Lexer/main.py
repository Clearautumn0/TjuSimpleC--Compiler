from tokensAndAnalysis import Lexer
from nfa import NFAGenerator
from dfa import nfa_to_dfa
from minimize_dfa import MinimizedDFA

code = "int main() { return 0; }"
lexer = Lexer()
tokens = lexer.tokenize(code)

print("Tokens:")
for token in tokens:
    print(f"{token[1]}: {token[0]}")

nfa_generator = NFAGenerator(tokens)
start_state = nfa_generator.build_nfa()

print("\nNFA Transitions:")
nfa_generator.display_nfa(start_state)

dfa = nfa_to_dfa(start_state)
print("\nDFA Transitions:")
dfa.display_dfa()

minimized_dfa = MinimizedDFA(dfa)
minimized_dfa.minimize()
print("\nMinimized DFA Transitions:")
minimized_dfa.display_minimized_dfa()
