# 词法分析器
目录结构：

```── lexer/               # 词法分析器的核心实现
│   ├── __init__.py      
│   ├── lexer.py         # 词法分析器的主要代码
│   ├── token.py         # 定义Token类
│   └── patterns.py      # 存放标记的正则表达式
├── tests/               # 测试相关文件
│   ├── __init__.py
│   ├── test_lexer.py   
│   └── sample_code.cmm  # 一些C--代码示例用于测试
├── examples/            # 示例文件
│   └── example.cmm      # 一些C--代码示例
└── README.md            # 项目简介


