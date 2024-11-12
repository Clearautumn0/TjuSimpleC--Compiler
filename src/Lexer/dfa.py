from collections import defaultdict

class DFAState:
    def __init__(self, nfa_states):
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

            symbol_to_states = defaultdict(set)
            for nfa_state in current_dfa_state.nfa_states:
                for symbol, next_states in nfa_state.transitions.items():
                    if symbol != "ε":
                        symbol_to_states[symbol].update(next_states)

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
