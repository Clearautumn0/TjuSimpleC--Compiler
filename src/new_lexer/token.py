'''
token实体类

构造时传入三个components: type, value, id

1. type: token的类型，如数字、字母、运算符等
2. value: token的值，如数字、字母、运算符等的具体值
3. id: token的唯一标识符，用于区分不同token

4. __repr__: 打印token测试用信息
5. __str__: 打印token信息


@author: 覃邱维
状态：完成
'''
class Token:
    def __init__(self, type, value,id):
        self.type = type    # 类型，例如 KW, IDN, OP
        self.value = value  # 字符的值
        self.id = id        # 可选的 ID（例如用于符号表中标识符的唯一标识符）

        def __repr__(self):
            return f"Token(type={self.type}, value={self.value}, id={self.id})"
        def __str__(self):
            return f"{self.value},\t<{self.type}, {self.id}>"
        
# Token 类型常量
KW = "KW"
IDN = "IDN"
SE = "SE"
OP = "OP"
INT = "INT"
FLOAT = "FLOAT"
CHAR = "CHAR"
STRING = "STRING"

def get_tokens(state, str_token, DFA):
    # 获取当前符号的 token 字符串表示
    state_label = DFA.state_labels[state]
    
    if state_label == "INT":
        return f"<INT,{str_token}>"
    if state_label == "FLOAT":
        return f"<FLOAT,{str_token}>"
    if state_label == "SE":
        return f"<SE,{state}>"
    if state_label == "OP":
        return f"<OP,{state}>"
    if state_label == "I&K" and symbols_table.get(str_token) == "KW":
        return f"<KW,{state}>"
    
    # 如果是标识符
    return f"<IDN,{str_token}>"