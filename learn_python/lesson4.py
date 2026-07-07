"""第4课：函数作为值、**kwargs、列表"""

# ══════════════════════════════════════════════
# 概念1：函数是一等公民（可以当变量传来传去）
# ══════════════════════════════════════════════

print("=== 概念1：函数也是值 ===")

def say_hello(name):
    return f"你好，{name}"

def say_bye(name):
    return f"再见，{name}"

# 函数名可以赋值给变量
my_func = say_hello   # 注意：没有()，不是调用
print(my_func("张三"))  # 通过变量调用 → 你好，张三

# 函数可以作为参数传给另一个函数
def greet(func, name):
    """接收一个函数作为参数"""
    result = func(name)
    return f"[打招呼] {result}"

print(greet(say_hello, "张三"))  # → [打招呼] 你好，张三
print(greet(say_bye, "李四"))    # → [打招呼] 再见，李四


# ══════════════════════════════════════════════
# 概念2：把函数存在对象里（项目里 Tool 的做法）
# ══════════════════════════════════════════════

print("\n=== 概念2：函数存在对象里 ===")

class MyTool:
    def __init__(self, name, fn):
        self.name = name           # 工具名
        self.fn = fn               # 把函数存起来

    def run(self, **kwargs):
        """执行存起来的函数"""
        print(f"调用工具: {self.name}")
        return self.fn(**kwargs)

# 定义几个工具函数
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

# 创建工具实例，每个工具绑一个函数
tool_add = MyTool("加法", add)
tool_mul = MyTool("乘法", multiply)

# 通过工具对象调用函数
print(tool_add.run(a=3, b=5))      # → 8
print(tool_mul.run(a=3, b=5))      # → 15

# 这和项目代码完全一样：
# Tool(name="read", description="...", fn=read_file)
# 就是把 read_file 这个函数存进了 Tool 对象里


# ══════════════════════════════════════════════
# 概念3：**kwargs（关键字参数）
# ══════════════════════════════════════════════

print("\n=== 概念3：**kwargs ===")

def demo_kwargs(**kwargs):
    """**kwargs 会收集所有 name=value 形式的参数"""
    print(f"收到了 {len(kwargs)} 个参数:")
    for key, value in kwargs.items():
        print(f"  {key} = {value}")

demo_kwargs(name="张三", age=25, city="北京")
# 输出：
# 收到了 3 个参数:
#   name = 张三
#   age = 25
#   city = 北京

# **kwargs 的真正威力：透传参数
def wrapper(func, **kwargs):
    """这个函数接收任意参数，透传给 func"""
    print(f"准备调用函数...")
    result = func(**kwargs)  # 把 kwargs 展开传进去
    print(f"调用完成，结果：{result}")
    return result

wrapper(add, a=10, b=20)  # → 30

# 项目里 execute(**kwargs) = 把参数透传给 fn
# tool.execute(path=".") → self.fn(path=".")


# ══════════════════════════════════════════════
# 概念4：文档字符串（docstring）
# ══════════════════════════════════════════════

print("\n=== 概念4：文档字符串 ===")

def my_function():
    """这是函数的说明文档

    可以写多行，描述参数和返回值
    用三个引号括起来
    """
    pass

# 用 help() 或 .__doc__ 查看文档
print(my_function.__doc__)  # → 这是函数的说明文档...


# ══════════════════════════════════════════════
# 概念5：函数返回列表，列表里放对象
# ══════════════════════════════════════════════

print("\n=== 概念5：列表里放对象 ===")

class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def __str__(self):
        return f"{self.name}: {self.score}分"

def get_students():
    """返回学生列表（类似 get_builtin_tools() 返回工具列表）"""
    return [
        Student("张三", 95),
        Student("李四", 82),
        Student("王五", 67),
    ]

students = get_students()
for s in students:
    print(s)  # 自动调 __str__
