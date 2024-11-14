
import sys
import os

# 添加 src 目录到 sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.abspath(os.path.join(current_dir, '.'))  # 这里将上一级目录指向 src 自己
if src_path not in sys.path:
    sys.path.append(src_path)
