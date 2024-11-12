import re

# 定义词法规则
LEXICAL_RULES = [
    ('KW', r'\b(int|float|char|void|return|const|main)\b'), #关键字（KW）：我们定义了几个具体的关键字，单独匹配即可
    ('OP', r'(!|\+|-|\*|\/|%|=|>|<|==|<=|>=|!=|&&|\|\|)'),  #运算符（OP）：由于运算符的数量有限，可以定义匹配模式来匹配特定的符号
    ('SE', r'(\(|\)|\{|\}|;|,)'),                           #界符（SE）：类似于运算符，直接枚举这些符号
    ('IDN', r'[A-Za-z_][A-Za-z0-9_]*'),                     #标识符（IDN）：由字母、数字和下划线组成，但不以数字开头
    ('INT', r'\b[0-9]+\b'),                                 #整数（INT）：一串数字即可
    ('FLOAT', r'\b[0-9]+\.[0-9]+(e[+-]?[0-9]+)?\b'),        #浮点数（FLOAT）：数字后跟小数点和可选的小数部分，允许科学计数法
    ('CHAR', r"'[^']'"),                                    #单字符（CHAR）：用单引号括起来的单个字符
    ('STR', r'"[^"]*"')                                     #字符串（STR）：用双引号括起来的字符串，可以是任意字符，但要避免非转义的双引号
]


# 构建NFA

# class NFAState:
#     def __init__(self):
#         self.transitions = {}  # symbol -> set of NFAState (可以是 epsilon 转移)
#         self.is_accept = False

#     def add_transition(self, symbol, state):
#         if symbol not in self.transitions:
#             self.transitions[symbol] = set()
#         self.transitions[symbol].add(state)

class NFAState:
    _id_counter = 0  # 用于生成唯一 ID ，方便调试

    def __init__(self):
        self.id = NFAState._id_counter  # 分配唯一 ID
        NFAState._id_counter += 1
        self.transitions = {}  # symbol -> set of NFAState
        self.is_accept = False

    def add_transition(self, symbol, state):
        if symbol not in self.transitions:
            self.transitions[symbol] = set()
        self.transitions[symbol].add(state)


class NFA:
    def __init__(self, start_state, accept_state):
        self.start_state = start_state
        self.accept_state = accept_state
        accept_state.is_accept = True  # 设置接受状态

    @staticmethod
    def basic(symbol):
        """创建一个基本的 NFA，包含一个符号"""
        start = NFAState()
        accept = NFAState()
        start.add_transition(symbol, accept)
        return NFA(start, accept)

    @staticmethod
    def epsilon():
        """创建一个只包含 epsilon 的 NFA"""
        start = NFAState()
        accept = NFAState()
        start.add_transition('ε', accept)
        return NFA(start, accept)

    @staticmethod
    def union(nfa1, nfa2):
        """并联操作 | ：创建一个新的 NFA，将两个 NFA 通过 epsilon 转移合并"""
        start = NFAState()
        accept = NFAState()
        start.add_transition('ε', nfa1.start_state)
        start.add_transition('ε', nfa2.start_state)
        nfa1.accept_state.add_transition('ε', accept)
        nfa2.accept_state.add_transition('ε', accept)
        nfa1.accept_state.is_accept = False
        nfa2.accept_state.is_accept = False
        return NFA(start, accept)

    @staticmethod
    def concatenate(nfa1, nfa2):
        """连接操作：连接两个 NFA"""
        nfa1.accept_state.is_accept = False
        nfa1.accept_state.add_transition('ε', nfa2.start_state)
        return NFA(nfa1.start_state, nfa2.accept_state)

    @staticmethod
    def kleene_star(nfa):
        """闭包操作 * ：将一个 NFA 转化为 Kleene 星操作 NFA"""
        start = NFAState()
        accept = NFAState()
        start.add_transition('ε', nfa.start_state)
        start.add_transition('ε', accept)
        nfa.accept_state.add_transition('ε', accept)
        nfa.accept_state.add_transition('ε', nfa.start_state)
        nfa.accept_state.is_accept = False
        return NFA(start, accept)
    
    def print_nfa(self):
        """打印 NFA 状态和转移"""
        visited = set()
        self._print_state(self.start_state, visited)

    def _print_state(self, state, visited):
        """递归地打印每个状态的转移"""
        if state.id in visited:
            return
        visited.add(state.id)

        # 打印状态 ID 和接受状态标记
        print(f"State {state.id}{' (accept)' if state.is_accept else ''}:")

        # 打印每个转移
        for symbol, states in state.transitions.items():
            for next_state in states:
                print(f"  --{symbol}--> State {next_state.id}")
        
        # 递归打印转移到的状态
        for states in state.transitions.values():
            for next_state in states:
                self._print_state(next_state, visited)


class RegexParser:
    def __init__(self, regex):
        self.regex = regex
        self.pos = 0

    def parse(self):
        return self.regex_union()

    def regex_union(self):
        """解析 | 运算"""
        left = self.regex_concat()
        while self.match('|'):
            right = self.regex_concat()
            left = NFA.union(left, right)
        return left

    def regex_concat(self):
        """解析连接运算"""
        left = self.regex_kleene()
        while self.pos < len(self.regex) and self.regex[self.pos] not in '|)':
            right = self.regex_kleene()
            left = NFA.concatenate(left, right)
        return left

    def regex_kleene(self):
        """解析闭包运算 *"""
        nfa = self.regex_basic()
        while self.match('*'):
            nfa = NFA.kleene_star(nfa)
        return nfa

    def regex_basic(self):
        """解析基本字符或 (expression)"""
        if self.match('('):
            nfa = self.regex_union()
            assert self.match(')'), "Unmatched parenthesis"
            return nfa
        elif self.match('ε'):
            return NFA.epsilon()
        else:
            return NFA.basic(self.next())

    def match(self, char):
        """匹配字符并移动游标"""
        if self.pos < len(self.regex) and self.regex[self.pos] == char:
            self.pos += 1
            return True
        return False

    def next(self):
        """返回当前字符并移动游标"""
        char = self.regex[self.pos]
        self.pos += 1
        return char

# 测试正则表达式生成 NFA
regex = "(a|b)*abb"
parser = RegexParser(regex)
nfa = parser.parse()

# 生成的 nfa 是一个包含所有转移和状态的 NFA 对象

# 打印 NFA 的结构
nfa.print_nfa()