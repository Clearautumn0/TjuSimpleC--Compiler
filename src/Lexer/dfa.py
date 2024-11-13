#DFA生成，随后输出结果是DFA对象，包含了DFA的起始状态和它所有的状态


from collections import defaultdict

class DFAState:
    def __init__(self, nfa_states):
        self.nfa_states = frozenset(nfa_states) # 使用不可变集合来唯一标识DFA状态
        self.transitions = {} # 存储DFA状态的转移关系
        self.is_accept = any(state.is_accept for state in nfa_states) # 判断是否为接受状态

class DFA:
    def __init__(self, start_state):
        self.start_state = start_state  # DFA 的起始状态
        self.states = {}  # 保存所有DFA状态
        self._build_dfa()  # 自动构建DFA

    def _build_dfa(self):
        queue = [self.start_state]
        visited = set()
        visited.add(self.start_state.nfa_states) # 记录已经访问过的DFA状态
        
        while queue:
            current_dfa_state = queue.pop(0)
            self.states[current_dfa_state.nfa_states] = current_dfa_state # 将状态添加到字典中

            symbol_to_states = defaultdict(set)
            for nfa_state in current_dfa_state.nfa_states: #对于当前的 DFA 状态，遍历其包含的所有 NFA 状态，收集所有符号（非 ε）的目标状态。
                for symbol, next_states in nfa_state.transitions.items():
                    if symbol != "ε": # 忽略 ε 转移
                        symbol_to_states[symbol].update(next_states) # 收集每个符号对应的NFA目标状态集

            for symbol, nfa_target_states in symbol_to_states.items():
                new_dfa_state = DFAState(nfa_target_states)
                current_dfa_state.transitions[symbol] = new_dfa_state

                if new_dfa_state.nfa_states not in visited:
                    visited.add(new_dfa_state.nfa_states)
                    queue.append(new_dfa_state)

    def display_dfa(self):
        for dfa_state in self.states.values():
            for symbol, next_dfa_state in dfa_state.transitions.items():
                print(f"DFA State {dfa_state.nfa_states} --{symbol}--> DFA State {next_dfa_state.nfa_states}")
"""
使用栈(stack) 来进行深度优先搜索,以找到从给定状态集合通过 ε 转移可以到达的所有状态。
closure 用于存储最终的 ε 闭包结果。
对于每个状态，检查是否存在 ε 转移，如果有，则将目标状态添加到 closure 中，并继续对目标状态计算 ε 闭包。
"""
def epsilon_closure(nfa_states):
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

def nfa_to_dfa(nfa_start_state):
    start_states = epsilon_closure({nfa_start_state})
    start_dfa_state = DFAState(start_states)
    dfa = DFA(start_dfa_state)
    return dfa
