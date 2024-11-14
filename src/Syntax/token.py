'''
定义Token类，用于存储词法分析的结果

Token(type, value, id)

type: 词法单元类型
value: 词法单元的值
id: 词法单元的序号

__str__方法用于打印Token对象



'''
class Token:
    def __init__(self, type, value,id):
        self.type = type
        self.value = value
        self.id = id





    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.id})"

    def __str__(self):
        return f"{self.type}    <{self.value}, {self.id}>"


