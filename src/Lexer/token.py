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
        self.type = type
        self.value = value
        self.id = id

        def __repr__(self):
            return f"Token(type={self.type}, value={self.value}, id={self.id})"
        def __str__(self):
            return f"{self.value},\t<{self.type}, {self.id}>"