'''
定义转换规则
'''
class TransformMap:
    def __init__(self, rec, now, next_state):
        self.rec = rec        # 输入字符
        self.now = now        # 当前状态
        self.next = next_state  # 转换后的状态

    def __repr__(self):
        return f"TransformMap(rec={self.rec}, now={self.now}, next={self.next})"
