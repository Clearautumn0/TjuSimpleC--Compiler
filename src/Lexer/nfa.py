class NFAState:
    def __init__(self, is_accept=False):
        self.transitions = {}
        self.is_accept = is_accept

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = []
        self.transitions[symbol].append(state)

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
