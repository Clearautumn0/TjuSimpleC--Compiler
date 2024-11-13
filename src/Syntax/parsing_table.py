'''
分析表构建函数
构造分析表M的算法如下：
(1) 对文法G的每个产生式A→α,执行第(2)和(3)步；
(2) 对每个终结符a∈FIRST(α), 把A→α加入M[A, a]中；
(3) 若ε∈ FIRST(α), 则对任何b∈FOLLOW(A), 把Aàε加入M[A, b]中；
(4) 把所有无定义的M[A, a]标上“出错标志”。






'''
from collections import defaultdict
from grammar import Grammar
from first_and_follow import FirstAndFollow







def list_to_string(list):
    """将列表转换为字符串"""
    # 使用 str.join() 方法将列表中的元素连接成一个字符串
    return ''.join(map(str, list))



class ParsingTable:
    def __init__(self,first_set,follw_set,grammar):

        self.first_set = first_set
        self.follw_set = follw_set
        self.grammar = grammar
        self.M = self.build_parsing_table()
    def build_parsing_table(self):
        """构造分析表"""
        grammar = self.grammar
        first_set = convert_keys_to_string(self.first_set)
        follw_set = self.follw_set
        M = defaultdict(lambda: defaultdict(list))
        for A, productions in grammar.items():
            for alpha_list in productions:
                # print(f"alpha_list = {alpha_list}")
                alpha = list_to_string(alpha_list)

                if alpha in first_set.keys():
                    # print(f"alpha = {alpha}")
                    # print(f"first[{alpha}]={first[alpha]}")
                    for a in first_set[alpha]:
                        if is_terminal(a):
                            M[A][a].append({A:alpha_list})
                            print(f"M[{A}, {a}] = {M[A][a]}")
                        if '$' in first_set[A]:
                            for b in follw_set[A]:
                                M[A][b].append({A:['$']})
                                print(f"M[{A}, {b}] = {M[A][b]}")
        return M

    def get_production_from_table(self,L,R):
        """获取分析表中某一行的某一列的值"""
        M = self.M
        if L in M and R in M[L]:
            return M[L][R]
        else:
            # 处理情况，比如返回一个默认值或抛出异常
            return "error"  # 或者 raise KeyError(f"Key {L} or {R} not found in table")







    def print_parsing_table(self):
        """打印分析表"""
        M = self.M
        print("Parsing Table:")
        for A in M:
            for a in M[A]:
                rules = M[A][a]
                print(f"M[{A}, {a}] = {rules if rules else '出错标志'}")



def is_terminal(symbol):
    new_parser = FirstAndFollow(grammar, '$', "E", "#")
    """判断符号是否为终结符"""
    if symbol in new_parser.terminals:
        return True
    else:
        return False


def convert_keys_to_string(original_dict):
    """检查字典的键是否为列表，如果是列表则转换为字符串"""
    new_dict = {}

    for key, value in original_dict.items():
        # 判断键是否是列表形式
        if isinstance(key, list):
            # 如果键是列表形式，则转换成字符串形式
            key_str = ''.join(key)
            new_dict[key_str] = value
        else:
            # 如果键不是列表，则直接添加到新字典
            new_dict[key] = value

    return new_dict






if __name__ == '__main__':
    grammar = Grammar()

    # 添加文法规则
    grammar.add_rule("E", ["T", "E'"])
    grammar.add_rule("E'", ["+", "T", "E'"])
    grammar.add_rule("E'", ["$"])
    grammar.add_rule("T", ["F", "T'"])
    grammar.add_rule("T'", ["*", "F", "T'"])
    grammar.add_rule("T'", ["$"])
    grammar.add_rule("F", ["(", "E", ")"])
    grammar.add_rule("F", ["i"])

    # 创建解析器对象
    new_parser = FirstAndFollow(grammar, '$', "E", "#")

    first = {
        "E": {'(', 'i'},
        "E'": {'+', '$'},
        "T": {'(', 'i'},
        "T'": {'*', '$'},
        "F": {'(', 'i'},
        "TE'":{'(','i'},
        "+TE'":{'+'},
        "FT'":{'(','i'},
        "*FT'":{'*'},
        "(E)":{'(' },
        "i":{'i'}
      }



    follow = new_parser.follow_sets

    print("First sets:")
    for key, value in first.items():
        print(f"{key}: {value}")

    print("Follow sets:")
    for key, value in follow.items():
        print(f"{key}: {value}")

    print("grammar rules:")
    for key, value in grammar.rules.items():
        print(f"{key}: {value}")
    # 构造分析表

    print(" parsing table:")
    t  = ParsingTable(first, follow, grammar.rules)
    M = t.build_parsing_table()


    t.print_parsing_table()
    print ("测试获取分析表中某一行的某一列的值")
    print(t.get_production_from_table("E","i"))
    # 打印分析表




    
