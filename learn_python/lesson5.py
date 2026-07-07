"""第5课：列表、字典操作、or、getattr、列表推导式"""

# ══════════════════════════════════════════════
# 概念1：or 的"默认值"用法
# ══════════════════════════════════════════════

print("=== 概念1：or 做默认值 ===")

# 项目代码：message.content or ""
# 意思：如果 content 有值就用它，没有就用 ""

def demo_or(value):
    result = value or "（默认值）"
    print(f"  输入: {repr(value)} → 结果: {result}")

print('or 的规则：左边为"假"就取右边')
demo_or("你好")        # → 你好（有内容，取左边）
demo_or("")           # → （默认值）（空字符串=假，取右边）
demo_or(None)         # → （默认值）（None=假，取右边）
demo_or(0)            # → （默认值）（0=假，取右边）

print("\n有什么用？API 可能返回空内容，or 保证不回 None:")
content = None
print(f"  {content or '（无内容）'}")


# ══════════════════════════════════════════════
# 概念2：列表操作（切片、合并、复制）
# ══════════════════════════════════════════════

print("\n=== 概念2：列表操作 ===")

# 项目代码第38行：msgs = list(messages)
# list() 可以把另一个列表复制一份，防止改坏原数据
original = [1, 2, 3]
copy = list(original)
copy.append(4)
print(f"  原列表: {original}")   # → [1, 2, 3]（没变）
print(f"  副本: {copy}")         # → [1, 2, 3, 4]（改了副本）

# 项目代码第41行：*msgs — 星号展开列表
# 把 [a, b] 展开成 a, b
a = [1, 2]
b = [3, 4]
combined = [0, *a, *b, 5]
print(f"  合并列表: {combined}")  # → [0, 1, 2, 3, 4, 5]

# 项目里就是这么用的：
msgs = [{"role": "user", "content": "你好"}]
system_msg = {"role": "system", "content": "你是助手"}
final = [system_msg, *msgs]  # → [system_msg, {"role":"user"...}]
print(f"  拼接消息: {final}")


# ══════════════════════════════════════════════
# 概念3：if 做"非空判断"
# ══════════════════════════════════════════════

print("\n=== 概念3：if 非空判断 ===")

# 项目代码第47行：if tools:
# 意思是"如果 tools 不是空的"
# 以下值在 if 里视为"假"：

test_values = [
    [],          # 空列表
    {},          # 空字典
    "",          # 空字符串
    None,        # 空
    0,           # 零
    [1, 2],      # 非空列表
    {"a": 1},    # 非空字典
    "hello",     # 非空字符串
]

for v in test_values:
    if v:
        print(f"  ✅ 真: {repr(v)}")
    else:
        print(f"  ❌ 假: {repr(v)}")


# ══════════════════════════════════════════════
# 概念4：getattr 动态获取属性
# ══════════════════════════════════════════════

print("\n=== 概念4：getattr ===")

# 项目代码第63行：getattr(message, "reasoning_content", None)
# 意思：从 message 对象里找 reasoning_content 属性
# 如果有就返回，没有就返回 None（不报错）

class Person:
    def __init__(self):
        self.name = "张三"
        self.age = 25

p = Person()

print(f"  getattr(p, 'name'): {getattr(p, 'name')}")      # → 张三
print(f"  getattr(p, 'age'): {getattr(p, 'age')}")        # → 25
print(f"  getattr(p, 'job', None): {getattr(p, 'job', None)}")  # → None（没有就返回默认值）

# 没有第三个参数的话，找不到就直接报错
# getattr(p, 'job')  # ← 如果运行这行：AttributeError


# ══════════════════════════════════════════════
# 概念5：列表推导式
# ══════════════════════════════════════════════

print("\n=== 概念5：列表推导式 ===")

# 项目代码第68行：[tool_call.model_dump() for tool_call in message.tool_calls]
# 意思：把 message.tool_calls 里的每个对象都调一次 .model_dump()，结果拼成新列表

# 普通写法
numbers = [1, 2, 3, 4, 5]
doubled = []
for n in numbers:
    doubled.append(n * 2)
print(f"  普通for循环: {doubled}")  # → [2, 4, 6, 8, 10]

# 列表推导式（一步完成）
doubled2 = [n * 2 for n in numbers]
print(f"  列表推导式: {doubled2}")  # → [2, 4, 6, 8, 10]

# 可以加 if 条件
evens = [n for n in numbers if n % 2 == 0]
print(f"  取偶数: {evens}")        # → [2, 4]

# 项目里的实际用法（简化版）：
class ToolCall:
    def __init__(self, name):
        self.name = name
    def model_dump(self):
        return {"name": self.name}

tool_calls = [ToolCall("ls"), ToolCall("read"), ToolCall("bash")]
result = [tc.model_dump() for tc in tool_calls]
print(f"  工具列表转字典: {result}")
# → [{"name": "ls"}, {"name": "read"}, {"name": "bash"}]


# ══════════════════════════════════════════════
# 概念6：client 调用（API 调用）
# ══════════════════════════════════════════════

print("\n=== 概念6：API 调用 ===")

# 项目代码第18行：
# client = OpenAI(api_key=..., base_url=...)
# response = client.chat.completions.create(model=..., messages=...)

# 这和我们之前学的没什么不同
# 只不过这个"函数"在远程服务器上
# client 就像一个遥控器，调它的方法 = 按遥控器按钮

print("""
OpenAI(...) 只是创建了一个"遥控器对象"
client.chat.completions.create(...) 是"按遥控器"
参数里的 model / messages 告诉服务器要做什么

整个过程 = 创建一个指向远程服务的连接对象
         → 调用对象的方法（内部发 HTTP 请求到 DeepSeek 服务器）
         → 服务器处理并返回结果
         → 程序拿到结果继续执行

这和普通的函数调用没有本质区别，只是"函数"在别人电脑上。
""")
