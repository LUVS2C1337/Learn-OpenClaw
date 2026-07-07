"""练习一：数据流水线"""

import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from core.node import Node, Flow


class NumberNode(Node):
    """接收数字，乘以2，返回 ("double", 结果)"""
    def exec(self, payload: Any) -> Tuple[str, Any]:
        result = payload * 2
        return "double", result


class StringNode(Node):
    """接收数字，转成字符串，返回 ("default", 字符串)"""
    def exec(self, payload: Any) -> Tuple[str, Any]:
        result = f"数字是: {payload}"
        return "default", result


class PrintNode(Node):
    """接收字符串，打印它"""
    def exec(self, payload: Any) -> Tuple[str, Any]:
        print(payload)
        return "default", None


# 连接：NumberNode → StringNode → PrintNode
num = NumberNode()
string = StringNode()
printer = PrintNode()

num - "double" >> string
string >> printer

# 启动
flow = Flow(num)
flow.run(5)
