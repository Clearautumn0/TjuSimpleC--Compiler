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






def build_parsing_table(first, follw, grammar):
    """构造分析表"""
    M = defaultdict(lambda: defaultdict(list))
    for A, productions in grammar.items():
        for alpha_list in productions:
            print(f"alpha_list = {alpha_list}")
            alpha = list_to_string(alpha_list)
            # print(f"first_keys= {first.keys()}")
            if alpha in first.keys():
                print(f"first[{alpha}] = {first[alpha]}")
                for a in first[alpha]:
                    if is_terminal(a):
                        M[A][a].append({A:alpha_list})
                        print(f"M[{A}, {a}] = {M[A][a]}")
                if '$' in first[alpha]:
                    for b in follw[A]:
                        M[A][b].append({A:['$']})
                        print(f"M[{A}, {b}] = {M[A][b]}")





def print_parsing_table(M):
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
    new_parser = FirstAndFollow(grammar, 'ε', "E", "#")

    first = {
        "E": {')', '#'},
        "E'": {')', '#'},
        "T": {'$', '+'},
        "T'": {'$', '+'},
        "F": {'$', '*'},
        "TF;":{'(','i'},
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
    M = build_parsing_table(first, follow, grammar.rules)
    # 打印分析表
    # print_parsing_table(M)




    
