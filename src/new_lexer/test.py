'''
仅作为测试使用
'''


from collections import deque, defaultdict

class Transition:
    def __init__(self, current_state, input_symbol, next_state):
        self.current_state = current_state
        self.input_symbol = input_symbol
        self.next_state = next_state

class FA:
    def __init__(self, start_state, final_states, transitions, input_symbols):
        self.start_state = start_state
        self.final_states = set(final_states)
        self.transitions = transitions  # 转换列表：Transition实例
        self.input_symbols = input_symbols

def getClosure(current_states, NFA):
    closure = set(current_states)  # 初始化闭包为当前状态集
    worklist = deque(current_states)  # 工作队列

    while worklist:
        state = worklist.popleft()
        # 遍历NFA的所有转换
        for transition in NFA.transitions:
            # 如果转换是ε转换，并且当前状态匹配，且新状态不在闭包中
            if transition.input_symbol == 'ε' and transition.current_state == state and transition.next_state not in closure:
                closure.add(transition.next_state)
                worklist.append(transition.next_state)  # 将新状态加入队列
    
    return closure  # 返回闭包

def getNextState(current_states, input_symbol, NFA):
    next_states = set()
    
    # 遍历当前状态集中的每个状态
    for state in current_states:
        # 遍历所有转换
        for transition in NFA.transitions:
            # 找到匹配的输入符号和当前状态
            if transition.current_state == state and transition.input_symbol == input_symbol:
                next_states.add(transition.next_state)
    
    # 对新的状态集合求闭包
    return getClosure(next_states, NFA)

def NFAdeterminization(NFA):
    DFA = FA(start_state=1, final_states=set(), transitions=[], input_symbols=NFA.input_symbols)
    processing_queue = deque()  # 待处理队列
    state_to_id = {}  # 映射状态集合到唯一ID
    next_id = 1  # 初始ID

    # 初始化DFA
    initial_closure = getClosure({NFA.start_state}, NFA)
    state_to_id[frozenset(initial_closure)] = next_id
    DFA.start_state = next_id
    DFA.states = {next_id}
    processing_queue.append(initial_closure)

    # 如果起始闭包包含NFA终态，则将DFA起始状态也标记为终态
    if any(state in NFA.final_states for state in initial_closure):
        DFA.final_states.add(next_id)

    while processing_queue:
        current_states = processing_queue.popleft()
        current_id = state_to_id[frozenset(current_states)]

        # 遍历所有输入符号
        for input_symbol in NFA.input_symbols:
            # 获取在输入符号下的下一个状态集合
            next_states = getNextState(current_states, input_symbol, NFA)
            if not next_states:
                continue  # 如果下一个状态集合为空，跳过

            # 检查状态集合是否已映射到DFA状态ID
            next_states_frozen = frozenset(next_states)
            if next_states_frozen not in state_to_id:
                next_id += 1
                state_to_id[next_states_frozen] = next_id
                DFA.states.add(next_id)
                processing_queue.append(next_states)

                # 检查是否包含NFA的终态
                if any(state in NFA.final_states for state in next_states):
                    DFA.final_states.add(next_id)

            # 创建DFA的转换
            DFA.transitions.append(Transition(current_id, input_symbol, state_to_id[next_states_frozen]))

    return DFA


# 定义转换和NFA
transitions = [
    Transition(0, 'ε', 1),
    Transition(1, 'a', 2),
    Transition(2, 'ε', 0),
    Transition(2, 'b', 3)
]

NFA = FA(start_state=0, final_states={3}, transitions=transitions, input_symbols={'a', 'b'})

# 进行NFA确定化
DFA = NFAdeterminization(NFA)

# 输出DFA的状态转换
for trans in DFA.transitions:
    print(f"DFA Transition: {trans.current_state} --{trans.input_symbol}--> {trans.next_state}")
