'''
文法类，用于表示文法规则

文法规则的形式为：

左侧非终结符 -> 右侧产生式1 

右侧产生式的形式为：

非终结符1 非终结符2... 非终结符n

其中，非终结符可以是终结符或非终结符。

文法类提供了以下方法：
- get_rule(): 获取文法规则字典
- add_rule(lhs, rhs): 添加一条文法规则
- get_productions(lhs): 获取给定非终结符的所有产生式
- output_grammar(path): 输出文法到文件
- __str__(): 返回文法规则的字符串表示




@author: <覃邱维>  在改 
'''



class Grammar:
    def __init__(self):
        self.rules={}
    def add_rule(self, lhs, rhs):
        """
        添加一条文法规则
        :param lhs: 左侧非终结符
        :param rhs: 右侧产生式（列表形式）
        """
        # print(lhs,rhs)
        lhs = lhs.strip()
        rhs = rhs
        if lhs not in self.rules:
            self.rules[lhs] = []
        self.rules[lhs].append(rhs)
        # print(self.rule)

    def get_productions(self,slf):
        """
        :return: 右侧产生式列表
        """
        return self.rules[slf]
    def output_grammar(self,path="../../output/grammar_rules.txt"):
        """
        输出文法到文件
        :param path: 文件路径
        """
        with open(path, 'w', encoding='utf-8') as f:
            for key, value in self.rules.items():
                # 将字典的每一对 key 和 value 写入文件
                f.write(f"{key}: {value}\n")

    def __str__(self):
        """
        返回文法规则的字符串表示
        """
        result = []
        for key in self.rules:
            for production in self.rules[key]:
                result.append(f"{key} -> {' '.join(production)}")
        return '\n'.join(result)



    def get_rules(self):
        """
        :return: 文法规则字典
        """
        return self.rules




# 测试
if __name__ == "__main__":
    grammar = Grammar()
    grammar.add_rule("compUnit", ["decl", "compUnit"])
    grammar.add_rule("compUnit", ["funcDef", "compUnit"])
    grammar.add_rule("compUnit", ["$"])
    grammar.add_rule("decl", ["typeSpec", "varDeclList", ";"])
    grammar.add_rule("typeSpec", ["int"])
    grammar.add_rule("varDeclList", ["varDecl", ",", "varDeclList"])
    grammar.add_rule("varDeclList", ["varDecl"])
    grammar.add_rule("varDecl", ["id", "[", "num", "]", "=", "num"])
    grammar.add_rule("varDecl", ["id", "=", "num"])
    grammar.add_rule("funcDef", ["typeSpec", "id", "(", "params", ")", "{", "compUnit", "}"])
    grammar.add_rule("params", ["param", ",", "params"])



    grammar.output_grammar()
    # 打印文法
    print(f"打印的内容：\n{grammar}")

    print(f"使用get_rule()方法获取文法规则：{grammar.get_rules()}")

    print(f"使用get_productions()方法获取compUnit右侧产生式：{grammar.get_productions("compUnit")}")