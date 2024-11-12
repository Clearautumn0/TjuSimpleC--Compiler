import re

# 定义词法单元类型和关键词、运算符、界符
KEYWORDS = ["int", "float", "char", "void", "return", "const", "main"]
OPERATORS = ["!", "+", "-", "*", "/", "%", "=", ">", "<", "==", "<=", ">=", "!=", "&&", "||"]
SEPARATORS = ["(", ")", "{", "}", ";", ","]
TOKEN_TYPES = {
    "KW": "关键字",
    "IDN": "标识符",
    "OP": "运算符",
    "SE": "界符",
    "INT": "整数",
    "FLOAT": "浮点数",
    "CHAR": "单字符",
    "STRING": "字符串"
}

# NFA 生成的状态节点
class NFAState:
    def __init__(self, is_accept=False):
        self.transitions = {}
        self.is_accept = is_accept

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

# 词法分析器
class Lexer:
    def __init__(self):
        self.tokens = []
        self.current_index = 0

    def tokenize(self, code):
        patterns = {
            "KW": r"\b(?:int|float|char|void|return|const|main)\b",
            "IDN": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
            "OP": r"[!+\-*/%=><&|=]+",
            "SE": r"[(){},;]",
            "INT": r"\b\d+\b",
            "FLOAT": r"\b\d+\.\d+\b",
            "CHAR": r"'.?'",
            "STRING": r'"[^"]*"'
        }

        token_regex = "|".join(f"(?P<{type}>{pattern})" for type, pattern in patterns.items())
        for match in re.finditer(token_regex, code):
            type = match.lastgroup
            value = match.group(type)
            self.tokens.append((value, TOKEN_TYPES[type]))
        return self.tokens

    def next_token(self):
        if self.current_index < len(self.tokens):
            token = self.tokens[self.current_index]
            self.current_index += 1
            return token
        return None

# NFA 生成器类
class NFAGenerator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.start_state = NFAState()
        self.accept_state = NFAState(is_accept=True)

    def build_nfa(self):
        current_state = self.start_state
        for token, token_type in self.tokens:
            next_state = NFAState()
            current_state.add_transition(token, next_state)
            current_state = next_state
        current_state.add_transition("ε", self.accept_state)
        return self.start_state

    def display_nfa(self, state=None, visited=None):
        if visited is None:
            visited = set()
        if state is None:
            state = self.start_state
        if state in visited:
            return
        visited.add(state)
        for symbol, next_states in state.transitions.items():
            for next_state in next_states:
                print(f"State {id(state)} --{symbol}--> State {id(next_state)}")
                self.display_nfa(next_state, visited)



from collections import defaultdict

class DFAState:
    def __init__(self, nfa_states):
        # 将 NFA 状态集合存储在 DFA 状态中
        self.nfa_states = frozenset(nfa_states)
        self.transitions = {}
        self.is_accept = any(state.is_accept for state in nfa_states)

class DFA:
    def __init__(self, start_state):
        self.start_state = start_state
        self.states = {}
        self._build_dfa()

    def _build_dfa(self):
        queue = [self.start_state]
        visited = set()
        visited.add(self.start_state.nfa_states)
        
        while queue:
            current_dfa_state = queue.pop(0)
            self.states[current_dfa_state.nfa_states] = current_dfa_state

            # 创建转移表，找到当前 NFA 状态集合中的每个符号的目标状态集合
            symbol_to_states = defaultdict(set)
            for nfa_state in current_dfa_state.nfa_states:
                for symbol, next_states in nfa_state.transitions.items():
                    if symbol != "ε":
                        symbol_to_states[symbol].update(next_states)

            # 为每个符号创建新的 DFA 状态
            for symbol, nfa_target_states in symbol_to_states.items():
                new_dfa_state = DFAState(nfa_target_states)
                current_dfa_state.transitions[symbol] = new_dfa_state

                # 如果该状态尚未访问过，则将其加入队列进行进一步探索
                if new_dfa_state.nfa_states not in visited:
                    visited.add(new_dfa_state.nfa_states)
                    queue.append(new_dfa_state)

    def display_dfa(self):
        for dfa_state in self.states.values():
            for symbol, next_dfa_state in dfa_state.transitions.items():
                print(f"DFA State {dfa_state.nfa_states} --{symbol}--> DFA State {next_dfa_state.nfa_states}")

# 示例：从之前的 NFA 转换为 DFA
def nfa_to_dfa(nfa_start_state):
    # 使用 ε-闭包找到 NFA 的起始状态集合
    start_states = epsilon_closure({nfa_start_state})
    start_dfa_state = DFAState(start_states)
    dfa = DFA(start_dfa_state)
    return dfa

def epsilon_closure(nfa_states):
    # 求 ε-闭包
    stack = list(nfa_states)
    closure = set(nfa_states)
    
    while stack:
        state = stack.pop()
        if "ε" in state.transitions:
            for next_state in state.transitions["ε"]:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
    return closure






# DFA 生成和最小化的类定义

class MinimizedDFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.minimized_states = []
        self.transitions = {}
        self.accept_token_map = {}

    def minimize(self):
        # 初始划分为接受状态和非接受状态
        accept_states = {state_id for state_id, state in self.dfa.states.items() if state.is_accept}
        non_accept_states = set(self.dfa.states) - accept_states
        partitions = [accept_states, non_accept_states]

        while True:
            new_partitions = []
            for group in partitions:
                split_map = defaultdict(set)
                for state in group:
                    key = tuple(self._find_target_partition(state, symbol, partitions)
                                for symbol in self.dfa.states[state].transitions.keys())
                    split_map[key].add(state)

                new_partitions.extend(split_map.values())

            if new_partitions == partitions:
                break
            partitions = new_partitions

        self._build_minimized_dfa(partitions)

    def _find_target_partition(self, state, symbol, partitions):
        target_state = self.dfa.states[state].transitions.get(symbol)
        for index, group in enumerate(partitions):
            if target_state in group:
                return index
        return None

    def _build_minimized_dfa(self, partitions):
        state_mapping = {}
        for index, group in enumerate(partitions):
            is_accept = any(self.dfa.states[state].is_accept for state in group)
            state_mapping[frozenset(group)] = index
            self.minimized_states.append(index)
            self.transitions[index] = {}

            # 映射接受状态到 token 类型
            for state in group:
                if self.dfa.states[state].is_accept:
                    token_type = self.dfa.states[state].accept_token_type
                    self.accept_token_map[index] = token_type

        for index, group in enumerate(partitions):
            representative = next(iter(group))
            for symbol, target_state in self.dfa.states[representative].transitions.items():
                target_partition = self._find_target_partition(representative, symbol, partitions)
                self.transitions[index][symbol] = target_partition

    def match_tokens(self, code):
        tokens = []
        current_state = 0
        current_token = ""
        for char in code:
            if char in self.transitions[current_state]:
                current_token += char
                current_state = self.transitions[current_state][char]
                if current_state in self.accept_token_map:
                    token_type = self.accept_token_map[current_state]
                    tokens.append((current_token, token_type))
                    current_token = ""
                    current_state = 0
            else:
                current_token = ""
                current_state = 0
        return tokens

# 示例代码
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

# 构建并显示 DFA
dfa = nfa_to_dfa(start_state)  # `start_state` 是之前 NFA 的起始状态
print("\nDFA Transitions:")
dfa.display_dfa()

# 示例：最小化 DFA
minimized_dfa = MinimizedDFA(dfa)  # `dfa` 是之前生成的 DFA
minimized_dfa.minimize()
minimized_dfa.display_minimized_dfa()
