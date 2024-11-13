'''
分析表构建函数
构造分析表M的算法如下：
(1) 对文法G的每个产生式Aàα,执行第(2)和(3)步；
(2) 对每个终结符a∈FIRST(α), 把Aàα加入M[A, a]中；
(3) 若ε∈ FIRST(α), 则对任何b∈FOLLOW(A), 把Aàε加入M[A, b]中；
(4) 把所有无定义的M[A, a]标上“出错标志”。


'''
from collections import defaultdict


def build_parsing_table(FIRST, FOLLOW, G):
    M = defaultdict(lambda: defaultdict(list))
    for A, rules in G.items():
        for rule in rules:
            for a in FIRST(rule.rhs):
                M[A, a].append(rule)
            if '$' in FIRST(rule.rhs):
                for b in FOLLOW(A):
                    M[A, b].append(rule)
    for A, rules in M.items():
        for a, rules_list in rules.items():
            if not rules_list:
                M[A, a] = 'error'
    return M





    
