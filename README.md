#TJUSimpleC--Compiler


本次作业的词法分析器以及语法分析器均基于python开发

## 项目结构
'''
├── docs

├── input

│   ├── extended_grammars.txt  //**修改后的文法**

│   ├── lex_input		\\项目测试代码保存位置

│   │   ├── test_base_1.c

│   │   ├── test_base_2.c

│   │   ├── test_base_3.c

│   │   ├── test_base_4.c

│   │   ├── test_struct.c

│   │   ├── test_switch.c

│   │   ├── test_union.c

├── output    

│   ├── grammar_rules.txt

│   ├── grammar_without_left_recursion.txt

│   ├── lex_output   //词法分析器分析结果

│   │   ├── lex1.txt

│   │   ├── lex1_1.txt

│   │   ├── lex1_2.txt

│   │   ├── lex1_7.txt

│   │   ├── lex2.txt

│   │   ├── lex3.txt

│   │   ├── lex4.txt

│   │   ├── lex_struct.txt

│   │   ├── lex_switch.txt

│   │   ├── lex_union.txt

│   ├── parser_output   //语法分析器分析结果

│   │   ├── syntax1.txt

│   │   ├── syntax2.txt

│   │   ├── syntax3.txt

│   │   ├── syntax4.txt

│   │   ├── syntax_struct.txt

│   │   ├── syntax_switch.txt

│   │   ├── syntax_union.txt

│   ├── parsing_table.html    //可视化的分析表内容

│   ├── predictive_parser.txt   

├── README.md

├── show_tree.py

├── src      //项目源代码

│   ├── config.py    //项目配置文件,这里配置项目的输入输出位置,是否打印可视化的分析表

│   ├── Lexer   **//词法分析器**

│   │   ├── Data_Deal.py

│   │   ├── dfa.py

│   │   ├── FA.py

│   │   ├── helper_func.py

│   │   ├── lexer.py    //**词法分析器入口**

│   │   ├── minimize_dfa.py

│   │   ├── README.md

│   │   ├── TransformMap.py

│   │   ├── __init__.py

│   ├── main.py    //**词法分析器+语法分析器入口**

│   ├── Syntax   //**语法分析器**

│   │   ├── eliminate_left_recursion.py

│   │   ├── first_and_follow.py

│   │   ├── grammar.py

│   │   ├── lexer_token.py

│   │   ├── parser.py    //**语法分析器入口**

│   │   ├── parsing_table.py

│   │   ├── PredictiveParser.py

│   │   ├── __init__.py

│   ├── utils   //**工具函数与工具类**

│   │   ├── lexer_util.py

│   │   ├── syntax_util.py

│   │   ├── __init__.py

│   ├── __init__.py

├── test

│   ├── test_lexer.py

│   ├── __init__.py

│   ├── 这里用来存放词法分析器&语法分析器的测试文件.md

'''

## 运行方式
测试运行词法分析器

`python ./src/Lexer/lexer.py`

测试运行语法分析器:您可以单独读取tokens来进行语法分析

`python ./src/Syntax/parser.py`

运行编译器,可以运行整体的编译器实现原始代码->tokens->语法分析情况

`python ./src/main.py`



## 编码环境:
python 3.11以上

## 开发环境
pycharm community 2024.1 

## 人员分工:
覃邱维:项目负责人

负责成员调度任务安排,负责整体的项目架构设计,实现语法分析器的分析表构建以及可视化部分,负责语法分析器中实体类的构以及数据的读入,负责展示ppt设计与实现,负责语法分析器的总体设计,负责新增文法的审查与校验.负责实验报告的组织与攥写.

王俊哲：项目成员

负责新增文法的编写与校验。语法分析器部分代码编写，实现语法分析器中消除左递归的功能，以及对语法分析器部分bug的修复。

李亮克：项目成员

负责词法分析器大部分代码的编写，负责部分NFA状态转换表的构建，NFA的确定化以及DFA的最小化的实现，同时为词法分析器编写了测试代码。

聂哲浩：项目成员

负责语法分析器部分代码的编写，实现语法分析器中FIRST和FOLLOW集合的计算，以及输出规约序列的功能。同时完成对语法分析模块的代码测试。

张浩然：项目成员

负责部分词法分析器的代码编写，部分文档撰写及排版工作。









