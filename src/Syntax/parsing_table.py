'''
分析表构建函数
构造分析表M的算法如下：
(1) 对文法G的每个产生式A→α,执行第(2)和(3)步；
(2) 对每个终结符a∈FIRST(α), 把A→α加入M[A, a]中；
(3) 若ε∈ FIRST(α), 则对任何b∈FOLLOW(A), 把Aàε加入M[A, b]中；
(4) 把所有无定义的M[A, a]标上“出错标志”。


'''
from collections import defaultdict

def is_terminal(symbol):
    return symbol.islower()







def build_parsing_table(FIRST, FOLLOW, G):
    M = defaultdict(lambda: defaultdict(list))

    for A, ruls in G.items() :
        for alpha in ruls:
            for a in alpha:
                if is_terminal(a):
                    M[A][a].append({A: [alpha]})
            if '$' in alpha:
                for b in FOLLOW[A]:
                    M[A][b].append({A: ["$"]})



    return M







def print_parsing_table(M):
    print("Parsing Table:")
    for A in M:
        for a in M[A]:
            rules = M[A][a]
            print(f"M[{A}, {a}] = {rules if rules else '出错标志'}")
if __name__ == '__main__':
    G = {
        'S': ['AB', 'a'],
        'A': ['aA', '$'],
        'B': ['bB', '$']
    }
    FIRST = {
    'S': {'a', '$'},
    'A': {'a', '$'},
    'B': {'b'}
    }

    FOLLOW = {
        'S': {'#'},
        'A': {'b', '#'},
        'B': {'#'}
    }
    M = build_parsing_table(FIRST, FOLLOW, G)
    print (M)
    print_parsing_table(M)

    
