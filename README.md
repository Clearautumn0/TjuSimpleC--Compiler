# TjuSimpleC--Compiler
天津大学2024编译原理大作业 C--编译器



├── docs/                   # 项目文档
│
├── input/                  # 输入的 C-- 源代码文件
│
├── output/                 # 输出的分析结果
│
├── src/                    # 源代码目录
│   ├── Lexer/              # 词法分析器模块
│   │   ├── __init__.py     # 初始化Lexer模块
│   │   ├── lexer.py        # 词法分析器的实现
│   │   └── token.py        # 定义Token类
│   │
│   ├── Syntax/            # 语法分析的相关模块
│   │   ├── __init__.py     # 初始化Grammar模块
│   │   ├── grammar.py      # 文法定义
│   │   ├── parser.py       # 语法分析器的实现
│   │   ├── ast.py          # 抽象语法树定义
│   │   └── error.py        # 错误处理
│   │
│   ├── utils/              # 工具类，如错误报告，调试工具
│   │   ├── __init__.py
│   │   └── utils.py
│   │
│   │     
    ├── test/               # 测试用例
    │   ├── __init__.py
    │   ├── test_lexer.py
    │   ├── test_parser.py
    