'''
文法类，用于表示文法规则

文法规则的形式为：

左侧非终结符 -> 右侧产生式1 

右侧产生式的形式为：

非终结符1 非终结符2... 非终结符n

其中，非终结符可以是终结符或非终结符。

文法类提供了以下方法：

- add_rule(lhs, rhs): 添加一条文法规则
- get_productions(lhs): 获取给定非终结符的所有产生式
- __str__(): 返回文法规则的字符串表示



@author: <覃邱维>  在改 
'''



class Grammar:
    def __init__(self):
        self.lhs=""
        self.rhs=[]
        self.rule={}
    def add_rule(self, lhs, rhs):
        """
        添加一条文法规则
        :param lhs: 左侧非终结符
        :param rhs: 右侧产生式（列表形式）
        """
        # print(lhs,rhs)
        self.lhs = lhs.strip()
        self.rhs = rhs
        if self.lhs not in self.rule:
            self.rule[self.lhs] = []
        self.rule[self.lhs].append(self.rhs)
        # print(self.rule)

    def get_productions(self):
        """
        :return: 右侧产生式列表
        """
        return self.rhs

    def __str__(self):
        """
        返回文法规则的字符串表示
        """
        result = []  # 创建一个空列表来存储结果
        for key, value_list in self.rule.items():
            for value in value_list:
                # 使用 '->' 连接键和对应的值，并添加到结果列表中
                result.append(f"{key} -> {' '.join(value)}")

        return '\n'.join(result)  # 将结果列表连接成字符串并返回

    def get_rule(self):
        """
        :return: 文法规则字典
        """
        return self.rule




# 测试
if __name__ == "__main__":
    grammar = Grammar()
    grammar.add_rule("compUnit", ["decl", "compUnit"])
    grammar.add_rule("compUnit", ["funcDef", "compUnit"])
    grammar.add_rule("compUnit", ["$"])

    # 打印文法
    print(f"打印的内容：\n{grammar}")

    print(f"使用get_rule()方法获取文法规则：{grammar.get_rule()}")

    # # 获取某个非终结符的产生式
    # print("Productions for 'compUnit':")
    # productions = grammar.get_productions()
    # for production in productions:
    #     print(production)
