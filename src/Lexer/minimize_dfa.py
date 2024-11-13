#DFA最小化，输出的是最小化后的状态集合

from collections import defaultdict

class MinimizedDFA:
    def __init__(self, dfa):
        self.dfa = dfa
        self.minimized_states = []
        self.transitions = {}

    def minimize(self):
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

        for index, group in enumerate(partitions):
            representative = next(iter(group))
            for symbol, target_state in self.dfa.states[representative].transitions.items():
                target_partition = self._find_target_partition(representative, symbol, partitions)
                self.transitions[index][symbol] = target_partition

    def display_minimized_dfa(self):
        for state, transitions in self.transitions.items():
            for symbol, target in transitions.items():
                print(f"State {state} --{symbol}--> State {target}")
