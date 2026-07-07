"""第7课：字典推导式、私有函数、if __name__"""

# ═══════════════════════════════════════════
# 概念1：字典推导式（第62行）
# ═══════════════════════════════════════════

print("=== 概念1：字典推导式 ===")

# 项目代码第62行：
# self.tool_map = {tool.name: tool for tool in self.tools}
# 意思：遍历 self.tools 这个列表，用每个 tool.name 当键，tool 本身当值

# 先看不加推导式怎么写
class Tool:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
    def __repr__(self):
        return f"Tool({self.name})"

tools_list = [
    Tool("read", "读文件"),
    Tool("bash", "执行命令"),
    Tool("ls", "列出目录"),
]

# 普通写法：建空字典 → for 循环 → 一个个放进去
tool_map = {}
for t in tools_list:
    tool_map[t.name] = t

print("普通for循环的结果:")
for name, t in tool_map.items():
    print(f"  {name} -> {t}")

# 字典推导式：一行搞定
tool_map2 = {t.name: t for t in tools_list}
print("\n字典推导式的结果:")
for name, t in tool_map2.items():
    print(f"  {name} -> {t}")

# 字典推导式 + if 条件
tool_map3 = {t.name: t for t in tools_list if t.name != "bash"}
print(f"\n过滤掉 bash 后的键: {list(tool_map3.keys())}")

# 为什么要搞成字典？—— 为了快速查找
# 列表查找：for t in tools_list: if t.name == "bash"  → 慢
# 字典查找：tool_map["bash"]  → 快
print(f"\n用名字直接查找: {tool_map['bash']}")  # 一步到位


# ═══════════════════════════════════════════
# 概念2：for-else（没用到，但帮你区分）
# ═══════════════════════════════════════════

print("\n=== 概念2补充：for循环里不要用else ===")

# 有些人会混淆，for 也可以接 else
# 但项目里没用这个语法，提一下避免你看到困惑
for i in range(3):
    print(f"  {i}")
else:
    print("  for循环正常结束（没有break）")

# 如果有 break，else 就不执行
for i in range(3):
    if i == 1:
        print("  break了")
        break
else:
    print("  这行不会执行")


# ═══════════════════════════════════════════
# 概念3：私有函数（_ 开头）
# ═══════════════════════════════════════════

print("\n=== 概念3：私有函数（_开头）===")

# 项目代码第107行：_safe_json_loads（以下划线开头）
# 第115行：_stringify_result（以下划线开头）

# 下划线开头的函数 = "这是内部使用的，外部不要直接调"
# 就像工具箱里的"内六角扳手"——能用，但建议你别碰

def public_function():
    """公开函数：外部可以随便调"""
    print("我是公开函数")

def _private_function():
    """私有函数：建议只在文件内部用"""
    print("我是私有函数（下划线开头）")

# 其实：Python 没有真正的"私有"
# _ 开头只是一个"约定"，表示"内部使用，别碰我"
# 你硬要调也能调，但别人看了会皱眉

print("""
命名惯例：
  def normal()    → 公开函数，"大家随便用"
  def _internal() → 内部函数，"小心使用"
  def __really_private() → 名字会被 Python 改写，更难意外调用
""")

# 项目里的实际作用：
# _safe_json_loads 只在 executor.py 内部用
# 外部只需要调 ToolExecutor 就够了
# _stringify_result 也是内部函数


# ═══════════════════════════════════════════
# 概念4：if __name__ == "__main__"
# ═══════════════════════════════════════════

print("\n=== 概念4：if __name__ == '__main__' ===")

# 项目代码第178-179行：
# if __name__ == "__main__":
#     demo()

# 这句话的意思是：只有直接运行这个文件时才执行
# 被别的文件 import 时就不执行

# 新建一个文件 helper.py：
#   print("我被 import 了")
#   if __name__ == "__main__":
#       print("我是被直接运行的")

# 场景1：python helper.py
#   输出：我被 import 了
#   输出：我是被直接运行的

# 场景2：在另一个文件里 import helper
#   输出：我被 import 了
#   （不输出"我是被直接运行的"那行）

print("""
为什么需要这个？

python executor.py
  → __name__ == "__main__" → True → 执行 demo()

from executor import ToolExecutor
  → __name__ == "executor" → False → 不执行 demo()
  → 只导入 ToolExecutor，不跑演示代码

这样同一个文件既可以当"程序"直接跑，
也可以当"模块"被别的文件引入。
""")


# ═══════════════════════════════════════════
# 概念5：函数返回列表推导式（第104行）
# ═══════════════════════════════════════════

print("=== 概念5：函数里直接 return 列表推导式 ===")

def execute_all_v1(tool_calls):
    """普通for循环版"""
    results = []
    for tc in tool_calls:
        results.append(f"执行了 {tc}")
    return results

def execute_all_v2(tool_calls):
    """列表推导式版（项目里的写法）"""
    return [f"执行了 {tc}" for tc in tool_calls]

# 结果完全一样
tools = [Tool("read", ""), Tool("bash", ""), Tool("ls", "")]
r1 = execute_all_v1(tools)
r2 = execute_all_v2(tools)
print(f"  v1: {r1}")
print(f"  v2: {r2}")

# ｀列表推导式 = for循环 + 列表.append() + return｀ 的四合一版本


# ═══════════════════════════════════════════
# 综合练习
# ═══════════════════════════════════════════

print("\n" + "=" * 50)
print("综合练习：字典推导式 + 私有函数 + __name__")
print("=" * 50)

# 场景：做一个课程成绩管理系统

# 私有函数：内部用来计算等级的
def _get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

class Student:
    def __init__(self, name, scores):
        self.name = name
        self.scores = scores  # 字典：{"语文": 95, "数学": 82}

    def average(self):
        return sum(self.scores.values()) / len(self.scores)

class GradeBook:
    def __init__(self, students):
        # 字典推导式：快速建索引
        self.students = {s.name: s for s in students}

    def get_student(self, name):
        return self.students.get(name, None)

    def report(self):
        """生成成绩报告"""
        result = {}
        for name, s in self.students.items():
            avg = s.average()
            result[name] = {
                "平均分": avg,
                "等级": _get_grade(avg),  # 调私有函数
            }
        return result

# 创建学生
students = [
    Student("张三", {"语文": 95, "数学": 88, "英语": 92}),
    Student("李四", {"语文": 72, "数学": 65, "英语": 78}),
    Student("王五", {"语文": 55, "数学": 48, "英语": 62}),
]

# 使用
gb = GradeBook(students)
report = gb.report()

for name, info in report.items():
    print(f"  {name}: 平均分 {info['平均分']:.1f}, 等级 {info['等级']}")


# 这个文件如果被 import，不会执行下面这个测试
if __name__ == "__main__":
    print("\n测试：通过名字找学生")
    s = gb.get_student("李四")
    if s:
        print(f"  找到: {s.name}")
    else:
        print("  没找到")
