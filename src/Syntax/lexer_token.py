'''
定义Token类，用于存储词法分析的结果

Token(type, value, id)

type: 词法单元类型
value: 词法单元的值
id: 词法单元的序号

__str__方法用于打印Token对象


@Author: <覃邱维>
'''
class LexerToken:
    def __init__(self, type, value, id):
        self.project_table = {
            "IDN": "Ident",
            "INT": "INT",
            "FLOAT": "FLOAT",
            "CHAR": "CHAR"
        }
        self.type = type
        self.value = self.project(value)
        self.id = id

    # 判断是否需要映射
    def project(self, value):
        if value not in ["KW", "OP", "SE", "EOF"]:
            return self.project_table[value]
        return value


    def __repr__(self):
        return f"LexerToken({self.type}, {self.value}, {self.id})"

    def __str__(self):
        return f"{self.type}    <{self.value}, {self.id}>"


