"""第2课练习：for循环、元组、运算符"""

# 1. for 循环
print("=== 1. for 循环 ===")
for i in range(5):
    print(f"这是第{i}次循环")


# 2. 元组
print("\n=== 2. 元组 ===")
def min_max(lst):
    """返回列表的最小值和最大值（元组）"""
    return min(lst), max(lst)

result = min_max([3, 7, 2, 9, 1])
print(f"结果是一个元组：{result}")
print(f"最小值：{result[0]}，最大值：{result[1]}")

# 拆包
low, high = result
print(f"拆包后：low={low}, high={high}")


# 3. 自定义 >> 运算符
print("\n=== 3. 自定义 >> 运算符 ===")

class PipeNode:
    """模拟 Node 里的 >> 运算符"""
    def __init__(self, name):
        self.name = name
        self.next_node = None

    def __rshift__(self, other):
        """a >> b 相当于 a 连接到 b"""
        self.next_node = other
        return other

    def run(self, data):
        print(f"{self.name} 收到: {data}")
        if self.next_node:
            self.next_node.run(data + 1)

# 连接：a >> b >> c
a = PipeNode("节点A")
b = PipeNode("节点B")
c = PipeNode("节点C")

a >> b >> c

# 启动
a.run(0)
