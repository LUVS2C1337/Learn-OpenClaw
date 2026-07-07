"""第6课：isinstance、json、dataclass、classmethod"""

import json

# ═══════════════════════════════════════════
# 练习1：isinstance 类型判断
# ═══════════════════════════════════════════

print("=== 练习1：isinstance 类型判断 ===")

def describe(value):
    """用 isinstance 判断一个值的类型"""
    if isinstance(value, str):
        return f"'{value}' 是字符串，长度{len(value)}"
    elif isinstance(value, int):
        return f"{value} 是整数"
    elif isinstance(value, list):
        return f"{value} 是列表，有{len(value)}个元素"
    elif isinstance(value, dict):
        return f"{value} 是字典，有{len(value)}个键"
    else:
        return f"{value} 是其他类型"

print(describe("hello"))
print(describe(42))
print(describe([1, 2, 3]))
print(describe({"a": 1}))


# ═══════════════════════════════════════════
# 练习2：json 和 isinstance 配合
# ═══════════════════════════════════════════

print("\n=== 练习2：安全的 JSON 解析 ===")

def safe_json_loads(value):
    """跟项目里的 _safe_json_loads 一样"""
    if isinstance(value, str):
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return {}
    return {}

# 测试各种情况
test_inputs = [
    '{"name": "张三", "age": 25}',  # 正常 JSON 字符串
    '{"path": "."}',                 # 正常 JSON 字符串
    "不是 JSON 格式",                # 不是 JSON
    123,                             # 不是字符串
    None,                            # None
]

for val in test_inputs:
    result = safe_json_loads(val)
    print(f"  输入: {repr(val)[:30]}... → 输出: {result}")


# ═══════════════════════════════════════════
# 练习3：dataclass
# ═══════════════════════════════════════════

print("\n=== 练习3：dataclass ===")

from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    score: float

# 不用写 __init__，直接就能用
s1 = Student("张三", 18, 95.5)
s2 = Student("李四", 19, 82.0)

print(f"  {s1}")  # 自动打印美观格式
print(f"  {s2}")
print(f"  {s1.name} 的成绩是 {s1.score}")


# ═══════════════════════════════════════════
# 练习4：classmethod
# ═══════════════════════════════════════════

print("\n=== 练习4：classmethod ===")

@dataclass
class Car:
    brand: str
    model: str
    year: int

    @classmethod
    def from_string(cls, text):
        """从字符串创建 Car，格式：'品牌,型号,年份'"""
        parts = text.split(",")
        return cls(
            brand=parts[0].strip(),
            model=parts[1].strip(),
            year=int(parts[2].strip()),
        )

    def description(self):
        return f"{self.year} {self.brand} {self.model}"

# 普通方式创建
c1 = Car("Toyota", "Camry", 2020)
print(f"  普通创建: {c1.description()}")

# 类方法从字符串创建
c2 = Car.from_string("Honda, Civic, 2022")
print(f"  类方法创建: {c2.description()}")

# 第三个
c3 = Car.from_string("Tesla, Model 3, 2023")
print(f"  类方法创建: {c3.description()}")


# ═══════════════════════════════════════════
# 练习5：组合应用（模仿项目代码）
# ═══════════════════════════════════════════

print("\n=== 练习5：组合应用 ===")

@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict

    @classmethod
    def from_api_response(cls, item):
        """从 API 返回的字典创建 ToolCall
        跟项目里 from_openai_item 一样
        """
        function = item.get("function", {})
        raw_args = function.get("arguments", {})

        # 如果参数是字符串，解析成字典
        if isinstance(raw_args, str):
            try:
                raw_args = json.loads(raw_args)
            except json.JSONDecodeError:
                raw_args = {}

        # 确保参数是字典
        if not isinstance(raw_args, dict):
            raw_args = {}

        return cls(
            id=item.get("id", ""),
            name=function.get("name", ""),
            arguments=raw_args,
        )

# API 返回的数据
api_response = {
    "id": "call_123",
    "type": "function",
    "function": {
        "name": "bash",
        "arguments": '{"command": "ls"}'
    }
}

tc = ToolCall.from_api_response(api_response)
print(f"  工具调用: {tc.name}")
print(f"  参数: {tc.arguments}")
print(f"  ID: {tc.id}")
