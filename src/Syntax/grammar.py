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
        # 使用字典来存储文法规则，键是非终结符，值是右侧产生式列表
        self.rules = {}

    def add_rule(self, lhs, rhs):
        """
        添加一条文法规则
        :param lhs: 左侧非终结符
        :param rhs: 右侧产生式（列表形式）
        """
        lhs = lhs.strip()
        rhs = [r.strip().split() for r in rhs]
        if lhs not in self.rules:
            self.rules[lhs] = []
        self.rules[lhs].extend(rhs)

    def get_productions(self, lhs):
        """
        获取给定非终结符的所有产生式
        :param lhs: 左侧非终结符
        :return: 右侧产生式列表
        """
        return self.rules.get(lhs, [])

    def __str__(self):
        """
        返回文法规则的字符串表示
        """
        output = []
        for lhs, rhs_list in self.rules.items():
            for rhs in rhs_list:
                output.append(f"{lhs} -> {' '.join(rhs)}")
        return "\n".join(output)

# 测试
if __name__ == "__main__":
    grammar = Grammar()
    grammar.add_rule("program", ["compUnit"])
    grammar.add_rule("compUnit", ["decl", "compUnit"])
    grammar.add_rule("compUnit", ["funcDef", "compUnit"])
    grammar.add_rule("decl", ["constDecl"])

    # 打印文法
    print(grammar)

    # 获取某个非终结符的产生式
    print("Productions for 'compUnit':")
    productions = grammar.get_productions("compUnit")
    for production in productions:
        print(production)
