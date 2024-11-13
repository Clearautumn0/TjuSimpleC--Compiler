from collections import deque, defaultdict
from src.new_lexer.FA import FA
from src.new_lexer.transform_map import TransformMap
from src.new_lexer.symbols_table import lex_trans_map

def getClosure(nows, NFA):
    closure = set(nows)  # 初始化闭包为当前状态集
    worklist = deque(nows)  # 工作队列

    while worklist:
        state = worklist.popleft()
        # 遍历NFA的所有转换
        for transition in NFA.transitions:
            # 如果转换是ε转换，并且当前状态匹配，且新状态不在闭包中
            if transition.rec == 'ε' and transition.now == state and transition.next not in closure:
                closure.add(transition.next)
                worklist.append(transition.next)  # 将新状态加入队列
    
    return closure  # 返回闭包


def getNextState(nows, rec, NFA):
    nexts = set()
    
    # 遍历当前状态集中的每个状态
    for state in nows:
        # 遍历所有转换
        for transition in NFA.transitions:
            # 找到匹配的输入符号和当前状态
            if transition.now == state and transition.rec == rec:
                nexts.add(transition.next)
    
    # 对新的状态集合求闭包
    return getClosure(nexts, NFA)


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
        nows = processing_queue.popleft()
        current_id = state_to_id[frozenset(nows)]

        # 遍历所有输入符号
        for rec in NFA.input_symbols:
            # 获取在输入符号下的下一个状态集合
            nexts = getNextState(nows, rec, NFA)
            if not nexts:
                continue  # 如果下一个状态集合为空，跳过

            # 检查状态集合是否已映射到DFA状态ID
            nexts_frozen = frozenset(nexts)
            if nexts_frozen not in state_to_id:
                next_id += 1
                state_to_id[nexts_frozen] = next_id
                DFA.states.add(next_id)
                processing_queue.append(nexts)

                # 检查是否包含NFA的终态
                if any(state in NFA.final_states for state in nexts):
                    DFA.final_states.add(next_id)

            # 创建DFA的转换
            DFA.transitions.append(TransformMap(rec, current_id, state_to_id[nexts_frozen]))

    return DFA


# # 定义转换和NFA
# transitions = [
#     TransformMap('ε', 0, 1),
#     TransformMap('a', 1, 2),
#     TransformMap('ε', 2, 0),
#     TransformMap('b', 2, 3)
# ]

NFA = FA(start_state=0, final_states={3}, transitions=lex_trans_map, input_symbols={'ε'})

# 进行NFA确定化
DFA = NFAdeterminization(NFA)

# 输出DFA的状态转换
for trans in DFA.transitions:
    print(f"DFA Transition: {trans.now} --{trans.rec}--> {trans.next}")
