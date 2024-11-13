class FA:
    def __init__(self):
        self.input_symbols = []  # 输入字符集
        self.states = set()  # 状态集合
        self.state_labels = {}  # 状态标签
        self.trans_map = set()  # 转换映射规则
        self.start = set()  # 初始状态集合
        self.final = set()  # 终态集合