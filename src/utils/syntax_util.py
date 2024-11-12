

from src.Syntax.grammar import Grammar


def load_from_file(file_path):
    grammars=[]#返回值
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue  # 忽略空行和注释行
            
            # 将文法规则分割为左侧和右侧
            lhs, rhs = line.split("->")
            lhs = lhs.strip()  # 去掉空格
            rhs_options = [r.strip() for r in rhs.split('|')]
            
            # 添加文法规则到 Grammar 中
            for rhs in rhs_options:
                grammar=Grammar()
                # 直接用 rhs 包含分号
                grammar.add_rule(lhs, rhs.strip().split())
                grammars.append(grammar)
    return grammars        
            
            
if __name__ == '__main__':
    
    grammars = load_from_file("../../input/grammars.txt")
    i =1
    for grammar in grammars:
        print(f"{i}. {grammar}")
        i+=1
