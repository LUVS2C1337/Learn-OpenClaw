"""回顾+实战：已学概念对照 + 今日实战
====================================
实战目标：终端待办事项管理器（Todo Manager）
功能：添加、列出、完成、删除任务，数据持久化
====================================
"""

# ═════════════════════════════════════════
# 第一部分：7课概念速查表（复习专用）
# ═════════════════════════════════════════

print("=" * 55)
print("7 课概念速查表")
print("=" * 55)

review = """
┌──────┬─────────────────────┬─────────────────────────────┐
│ 第1课 │  import / 变量 / 字典 │ from pathlib import Path     │
│       │  类 / self / raise   │ shared = {}                 │
│       │                     │ class Node:                 │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第2课 │  for 循环 / 元组      │ for i in range(n)           │
│       │  拆包 / 运算符重载    │ return "a", "b"             │
│       │                     │ a, b = func()               │
│       │                     │ def __rshift__(self, other) │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第3课 │  if / while / None   │ if x > 0:                   │
│       │  try/except / .get() │ while curr:                 │
│       │  重试机制            │ d.get("key", None)          │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第4课 │  函数当值传递         │ def fn(): ...              │
│       │  **kwargs            │ Tool(..., fn=fn)            │
│       │  函数存在对象里       │ def execute(**kwargs)       │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第5课 │  or 默认值 / 列表操作  │ content or ""               │
│       │  getattr / 列表推导式 │ [x*2 for x in lst]         │
│       │  if 非空判断          │ if tools:                  │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第6课 │  isinstance / json    │ isinstance(x, str)         │
│       │  dataclass            │ json.loads / json.dumps    │
│       │  classmethod          │ @dataclass                 │
│       │                       │ @classmethod               │
├──────┼─────────────────────┼─────────────────────────────┤
│ 第7课 │  字典推导式            │ {k: v for k, v in lst}     │
│       │  私有函数 _           │ def _internal():           │
│       │  if __name__         │ import vs 直接运行          │
│       │  综合运用             │ 全部合起来写项目            │
└──────┴─────────────────────┴─────────────────────────────┘

还有3个额外技巧：
  🔧 print(f"x={x}")          → 调试第一招
  🔧 python 交互模式           → 试小代码
  🔧 Traceback 从下往上看      → 看报错
"""
print(review)

# ═════════════════════════════════════════
# 第二部分：实战项目 — Todo Manager
# ═════════════════════════════════════════

print("=" * 55)
print("实战项目：Todo Manager")
print("=" * 55)

import json
from pathlib import Path

# ── 用 dataclass（第6课）定义任务 ──
# 就像项目里 @dataclass class ToolCall:

from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class TodoItem:
    """一条待办事项（和项目里的 ToolCall 一样结构）"""
    id: int
    title: str
    done: bool = False
    created_at: str = ""

    def __post_init__(self):
        """dataclass 初始化后自动调用（补充默认值）"""
        if not self.created_at:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self):
        """转成字典（用于存 JSON）"""
        return {
            "id": self.id,
            "title": self.title,
            "done": self.done,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典创建（classmethod，就像项目里的 ToolCall.from_openai_item）"""
        return cls(
            id=data["id"],
            title=data["title"],
            done=data.get("done", False),
            created_at=data.get("created_at", ""),
        )


# ── TodoManager 类（管理所有任务）──
# 用了：类（第1课）、字典推导式（第7课）、私有函数（第7课）

TODO_FILE = Path("todos.json")

class TodoManager:
    """待办事项管理器（和项目里的 ToolExecutor 地位一样）"""

    def __init__(self):
        self.items: list[TodoItem] = []
        self._next_id = 1
        self._load()  # 启动时自动从文件加载

    # ── 私有函数（第7课）：内部方法 ──

    def _load(self):
        """从 JSON 文件加载任务（if __name__ 的对应：导入时不执行）"""
        if not TODO_FILE.exists():
            self.items = []
            return

        try:
            text = TODO_FILE.read_text(encoding="utf-8")              # 文件读取（read.py）
            data = json.loads(text)                                    # json 解析（第6课）
            self.items = [TodoItem.from_dict(d) for d in data]         # 列表推导式（第5课）
            if self.items:
                self._next_id = max(item.id for item in self.items) + 1  # for 循环求最大
        except (json.JSONDecodeError, KeyError) as e:                  # try/except（第3课）
            print(f"  读取数据文件出错: {e}")
            self.items = []

    def _save(self):
        """把任务列表存到 JSON 文件"""
        data = [item.to_dict() for item in self.items]                 # 列表推导式（第5课）
        TODO_FILE.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),            # json.dumps（第6课）
            encoding="utf-8",
        )

    def _find_item(self, item_id):
        """根据 id 找任务（私有函数，内部用）"""
        # 字典推导式的等价用法：{item.id: item for item in self.items}
        for item in self.items:                                        # for 循环（第2课）
            if item.id == item_id:                                      # if 判断（第3课）
                return item
        return None                                                     # 没找到返回 None（第3课）

    # ── 公开函数：外部调用 ──

    def add(self, title: str):
        """添加新任务"""
        if not title or not title.strip():                              # or 默认值（第5课）+ if 非空判断（第5课）
            print("  ❌ 标题不能为空")
            return

        # isinstance 检查（第6课）
        if not isinstance(title, str):
            print("  ❌ 标题必须是文字")
            return

        item = TodoItem(
            id=self._next_id,
            title=title.strip(),
        )
        self._next_id += 1
        self.items.append(item)
        self._save()                                                    # 自动存文件
        print(f"  ✅ 已添加: [{item.id}] {item.title}")

    def list_all(self):
        """列出所有任务"""
        if not self.items:                                              # if 非空判断（第5课）
            print("  📭 暂无待办事项")
            return

        print(f"\n  {'ID':<4} {'状态':<8} {'创建时间':<18} 标题")
        print(f"  {'--':<4} {'----':<8} {'--------':<18} ----")

        for item in self.items:                                         # for 循环（第2课）
            status = "✅ 已完成" if item.done else "⏳ 待办"
            print(f"  {item.id:<4} {status:<8} {item.created_at}  {item.title}")

        # 统计信息（字典推导式的实际应用）
        done_count = len([i for i in self.items if i.done])             # 列表推导式 + if
        todo_count = len(self.items) - done_count
        print(f"\n  共 {len(self.items)} 项（{todo_count} 项待办, {done_count} 项已完成）")

    def mark_done(self, item_id: int):
        """标记任务为已完成"""
        try:
            item_id = int(item_id)                                      # 类型转换，可能抛 ValueError
        except (ValueError, TypeError):                                 # try/except（第3课）
            print(f"  ❌ 无效的 ID: {item_id}")
            return

        item = self._find_item(item_id)
        if item is None:                                                # if + None 判断（第3课）
            print(f"  ❌ 未找到 ID 为 {item_id} 的任务")
            return

        if item.done:                                                   # if/else（第3课）
            print(f"  ⚠️  任务 [{item_id}] 已经完成了")
        else:
            item.done = True
            self._save()
            print(f"  ✅ 任务 [{item_id}] 标记为已完成")

    def delete(self, item_id: int):
        """删除任务"""
        # isinstance 检查（第6课）
        if not isinstance(item_id, int):
            print(f"  ❌ ID 必须是数字")
            return

        original_len = len(self.items)
        self.items = [item for item in self.items if item.id != item_id]  # 列表推导式（第5课）

        if len(self.items) == original_len:                              # if 判断（第3课）
            print(f"  ❌ 未找到 ID 为 {item_id} 的任务")
        else:
            self._save()
            print(f"  ✅ 已删除 ID 为 {item_id} 的任务")


# ── if __name__（第7课）：直接运行时才进入交互模式 ──

# 这个函数的写法参考了项目里 _stringify_result（私有函数）
def _show_menu():
    """显示菜单"""
    print(f"""
╔══════════════════════════════╗
║        TODO 管理器           ║
╠══════════════════════════════╣
║  add    <标题>   添加任务    ║
║  list             列出所有   ║
║  done  <ID>      完成任务   ║
║  del   <ID>      删除任务   ║
║  help             显示菜单   ║
║  quit             退出       ║
╚══════════════════════════════╝
""")


# 这个函数是"函数作为值传递"（第4课）的演示
def get_command_handler(command):
    """根据命令返回对应的处理函数
    就像项目里：Tool(name="ls", fn=ls_function)"""
    commands = {
        "add": "add",
        "list": "list",
        "done": "done",
        "del": "del",
        "delete": "del",
    }
    return commands.get(command, None)


# 主交互循环（参考了 chatbot 的 while True 模式）
def main():
    todo = TodoManager()

    # 最开始的提醒（or 默认值用法）
    first_run = input("首次使用？(y/n): ").strip().lower() or "n"
    if first_run == "y":
        todo.add("学习 Python 回顾课")
        todo.add("完成 Todo Manager 实战")
        todo.add("继续 AI Agent 学习")

    _show_menu()

    while True:  # while 循环（第3课）
        try:     # try/except（第3课）
            cmd = input("\n> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n退出。")
            break

        if not cmd:                     # if 非空判断（第5课）
            continue

        # 拆包（第2课）
        parts = cmd.split(maxsplit=1)    # → ["add", "买牛奶"] 或 ["list"]
        action = parts[0].lower()
        arg = parts[1] if len(parts) > 1 else ""

        if action == "quit" or action == "q" or action == "exit":
            print("再见！")
            break
        elif action == "help":
            _show_menu()
        elif action == "list":
            todo.list_all()
        elif action == "add":
            todo.add(arg)
        elif action == "done":
            # 类方法 + 错误处理（第6课 + 第3课）
            try:
                todo.mark_done(int(arg))
            except ValueError:
                print("  ❌ 请指定数字ID，如: done 1")
        elif action == "del" or action == "delete":
            try:
                todo.delete(int(arg))
            except ValueError:
                print("  ❌ 请指定数字ID，如: del 1")
        else:
            print(f"  未知命令: {action}，输入 help 查看帮助")


if __name__ == "__main__":  # 第7课
    main()
