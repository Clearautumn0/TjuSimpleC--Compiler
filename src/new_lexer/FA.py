'''
有限自动机结构定义
'''
from collections import deque, defaultdict

class FA:
    def __init__(self, start_state, final_states, transitions, input_symbols):
        self.start_state = start_state
        self.final_states = set(final_states)
        self.transitions = transitions  # 转换列表：Transition实例
        self.input_symbols = input_symbols