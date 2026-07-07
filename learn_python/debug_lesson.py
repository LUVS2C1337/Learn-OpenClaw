"""调试课：Python 报错怎么看、怎么自己查问题"""
import json

# ═══════════════════════════════════════════
# 第一部分：看懂报错信息（Traceback）
# ═══════════════════════════════════════════

print("=" * 50)
print("Part 1: 看懂报错信息")
print("=" * 50)

# 故意写一个有 bug 的代码

def get_user_info(user_id):
    users = {
        1: {"name": "张三", "age": 25},
        2: {"name": "李四", "age": 30},
    }
    return users[user_id]

def get_user_age(user_id):
    info = get_user_info(user_id)
    return info["age"]

# 运行看看报错
try:
    age = get_user_age(3)
    print(f"年龄: {age}")
except Exception as e:
    print("发生错误，但从下往上看 tracback：")
    print()

# 我们换一个能跑的，用 print 看看实际数据

print("\n先用正常数据看看返回值是什么：")
info = get_user_info(1)
print(f"  get_user_info(1) 返回: {info}")
print(f"  类型: {type(info)}")
age = get_user_age(1)
print(f"  get_user_age(1) 返回: {age}")

# ═══════════════════════════════════════════
# 第二部分：调试第一招 — print 大法
# ═══════════════════════════════════════════

print("\n" + "=" * 50)
print("Part 2: print 调试法（最常用）")
print("=" * 50)

# 假设我有这段代码，不知道哪里出了问题
def process_data(items):
    """处理数据，但不知道哪里不对"""
    result = []
    for item in items:
        # 加 print 看每一步
        print(f"  [调试] 当前处理: {repr(item)}, 类型: {type(item).__name__}")

        if isinstance(item, str):
            processed = item.upper()
        elif isinstance(item, (int, float)):
            processed = item * 2
        else:
            processed = str(item)

        print(f"  [调试] 处理后: {repr(processed)}")
        result.append(processed)

    print(f"  [调试] 最终结果: {result}")
    return result

# 正常调用
data = ["hello", 42, 3.14]
result = process_data(data)
print(f"  返回结果: {result}")

# ═══════════════════════════════════════════
# 第三部分：调试第二招 — type() 和 dir()
# ═══════════════════════════════════════════

print("\n" + "=" * 50)
print("Part 3: 不知道变量是什么类型时")
print("=" * 50)

def mystery_function(x):
    """你不知道 x 是什么，用 print 查"""
    print(f"  x 的值: {repr(x)}")
    print(f"  x 的类型: {type(x)}")

    if hasattr(x, "__len__"):
        print(f"  x 的长度: {len(x)}")

    # 如果是字典，看有哪些键
    if isinstance(x, dict):
        print(f"  字典的键: {list(x.keys())}")

    return x

# 测试
mystery_function("hello")
print()
mystery_function({"name": "张三", "age": 25, "scores": [90, 85, 92]})

# ═══════════════════════════════════════════
# 第四部分：调试第三招 — try/except 抓错误
# ═══════════════════════════════════════════

print("\n" + "=" * 50)
print("Part 4: try/except 抓错误 + 看详细信息")
print("=" * 50)

def risky_function(value):
    """这个函数可能出错"""
    result = value + 1
    result = result.upper()
    return result

def safe_call(value):
    """安全调用，抓住错误并打印详细信息"""
    try:
        result = risky_function(value)
        return result
    except Exception as e:
        print(f"  ❌ 出错了！")
        print(f"  错误类型: {type(e).__name__}")
        print(f"  错误信息: {e}")
        print(f"  传入的值: {repr(value)}, 类型: {type(value).__name__}")
        return None

# 用数字调用会出错
print("测试1：传数字")
safe_call(42)

print("\n测试2：传字符串（正常）")
safe_call("hello")

# ═══════════════════════════════════════════
# 第五部分：项目代码的真实报错分析
# ═══════════════════════════════════════════

print("\n" + "=" * 50)
print("Part 5: 项目代码的真实报错怎么看")
print("=" * 50)

print("""
当项目报错时，按这个顺序看：

示例报错：
────────────────────────────────────────
Traceback (most recent call last):
  File "tools\\executor.py", line 179, in <module>     ← ④ 执行入口
    demo()
  File "tools\\executor.py", line 128, in demo         ← ③ 调用 demo
    executor = ToolExecutor()
  File "tools\\executor.py", line 61, in __init__       ← ② 初始化出错
    self.tools = get_builtin_tools()
  File "tools\\builtins\\rag_search.py", line 30        ← ① 真正出错的位置
    embedding_client = OpenAI(
openai.OpenAIError: The api_key client option must be set
────────────────────────────────────────

看的方法：从下往上！
  第1步（最下面一行）：错误类型 + 错误原因
    → openai.OpenAIError: api_key 没设置

  第2步（往上一行）：哪个文件的哪一行
    → rag_search.py 第 30 行，调用 OpenAI() 时出错

  第3步：回溯调用链
    → executor.py → get_builtin_tools() → rag_search.py → OpenAI()
    知道调用链后，你就知道哪里传错了

常见的错误类型：
  NameError           → 变量名拼写错了
  TypeError           → 类型不对（字符串+数字之类的）
  ValueError          → 值不对（int("abc") 之类的）
  KeyError            → 字典里没有这个键
  IndexError          → 列表下标越界
  AttributeError      → 对象没有这个属性
  ModuleNotFoundError → import 的模块没装
  FileNotFoundError   → 文件不存在
""")

# ═══════════════════════════════════════════
# 第六部分：和 AI 配合调试
# ═══════════════════════════════════════════

print("=" * 50)
print("Part 6: 和 AI 配合调试（用 print 帮我定位）")
print("=" * 50)

print("""
你在 VS Code 里写代码遇到报错时，告诉我三样东西：

  1. 报错信息全文（从 Traceback 开始全部复制）
  2. 你写的代码
  3. 你想做什么

示例：
──────────
我：
"我写了这个代码：
   data = {"name": "张三"}
   print(data["age"])

   报错：KeyError: 'age'"

你：
"字典 data 里只有 name 这个键，没有 age。
用 data.get('age', '没找到') 就不会报错了。"
──────────

高级技巧：print 配合 f-string

  x = [1, 2, 3]
  print(f"x = {x}")             # 变量值
  print(f"x 的类型 = {type(x)}")  # 变量类型
  print(f"x 的长度 = {len(x)}")   # 变量长度

  不用写很多行，一行全打出来：
  print(f"x={x}, type={type(x).__name__}, len={len(x)}")
""")
