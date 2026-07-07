"""文件读写（Path 操作）
通过项目里的 read.py 学文件读写
"""

from pathlib import Path

print("=" * 55)
print("1. 创建 Path 对象")
print("=" * 55)

# Path 就是把"路径"变成一个对象，不再拼字符串

# 字符串方式（容易出错）
path1 = "D:/CC/Learn-OpenClaw" + "/" + "data" + "/" + "test.txt"

# Path 方式（安全，自动处理分隔符）
path2 = Path("D:/CC/Learn-OpenClaw") / "data" / "test.txt"
path3 = Path.cwd()                    # 当前工作目录
path4 = Path.home()                    # 用户主目录 C:\Users\armstrong

print(f"Path.cwd():  {path3}")
print(f"Path.home(): {path4}")
print(f"拼接路径:    {path2}")


print("\n" + "=" * 55)
print("2. 获取文件信息")
print("=" * 55)

# 项目代码 read.py 里用到的各种属性
current = Path("learn_python/file_searcher.py")

# 必须先用 resolve() 转成绝对路径
current = current.resolve()
print(f"绝对路径:    {current}")
print(f"文件名:      {current.name}")          # file_searcher.py
print(f"名字(不含后缀): {current.stem}")          # file_searcher
print(f"后缀:        {current.suffix}")         # .py
print(f"父目录:      {current.parent}")         # D:\CC\Learn-OpenClaw\learn_python
print(f"再上一级:    {current.parent.parent}")  # D:\CC\Learn-OpenClaw

# 这些对应项目代码 read.py 第 30-35 行：
#
# if cwd:
#     file_path = Path(cwd) / path    # 拼接工作目录
# else:
#     file_path = Path(path)
# file_path = file_path.resolve()      # 转绝对路径


print("\n" + "=" * 55)
print("3. 文件存在判断")
print("=" * 55)

# 项目代码 read.py 第 37-41 行
file1 = Path("learn_python/file_searcher.py").resolve()
file2 = Path("不存在的文件.txt").resolve()

print(f"文件1 是否存在: {file1.exists()}")     # True
print(f"文件2 是否存在: {file2.exists()}")     # False

if file1.exists():
    print(f"是文件吗: {file1.is_file()}")      # True
    print(f"是目录吗: {file1.is_dir()}")       # False

# 项目里的用法：
# if not file_path.exists():
#     raise FileNotFoundError(f"File not found: {path}")


print("\n" + "=" * 55)
print("4. 读文件内容")
print("=" * 55)

# 项目代码 read.py 第 44 行
# content = file_path.read_text(encoding="utf-8")

readme = Path("CLAUDE.md")
if readme.exists():
    # .read_text() 一行读取全部
    content = readme.read_text(encoding="utf-8")
    lines = content.split("\n")
    print(f"CLAUDE.md 共 {len(lines)} 行，{len(content)} 个字符")
    print(f"前 5 行:")
    for i, line in enumerate(lines[:5], 1):
        print(f"  {i}: {line}")


print("\n" + "=" * 55)
print("5. 写文件内容")
print("=" * 55)

# write_text() 写文件（不存在就创建，存在就覆盖）
test_file = Path("learn_python/test_write.txt")
test_file.write_text("这是第一次写入的内容\n这是第二行", encoding="utf-8")
print(f"写入成功: {test_file.resolve()}")
print(f"写入后读取验证: {test_file.read_text(encoding='utf-8')}")

# 追加内容（用 open 模式 a）
with open(test_file, "a", encoding="utf-8") as f:
    f.write("\n这是追加的第三行")
print(f"追加后内容:\n{test_file.read_text(encoding='utf-8')}")

# 清理
test_file.unlink()  # 删除文件
print(f"\n已删除测试文件")


print("\n" + "=" * 55)
print("6. 目录操作（配合项目代码 ls.py）")
print("=" * 55)

dir_path = Path("core")
if dir_path.exists() and dir_path.is_dir():
    print(f"core 目录的内容:")
    for entry in dir_path.iterdir():      # 列出目录
        suffix = "/" if entry.is_dir() else ""
        print(f"  {entry.name}{suffix}")


print("\n" + "=" * 55)
print("7. 递归搜索（配合项目代码 find.py）")
print("=" * 55)

print(f"所有 exercise 开头的文件:")
for p in Path(".").rglob("exercise*"):   # rglob = 递归搜索
    if p.is_file():
        print(f"  {p}")


print("\n" + "=" * 55)
print("8. 综合：模仿项目 read.py 的 offset/limit")
print("=" * 55)

def my_read(path: str, offset: int = 1, limit: int = None):
    """模仿项目 read.py：按行号范围读取文件

    项目代码 read.py 第 48-60 行就是这个逻辑
    """
    file_path = Path(path).resolve()
    if not file_path.exists():
        print(f"文件不存在: {path}")
        return ""

    content = file_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    # offset 从 1 开始（项目也是 1-indexed）
    start = max(0, offset - 1)
    if start >= len(lines):
        print(f"起始行 {offset} 超过总行数 {len(lines)}")
        return ""

    if limit:
        end = min(start + limit, len(lines))
    else:
        end = len(lines)

    selected = lines[start:end]
    result = "\n".join(selected)

    print(f"读取 {path} 第 {offset}-{end} 行 (共 {len(lines)} 行)")
    return result

# 测试
content = my_read("core/node.py", offset=1, limit=10)
print("\n--- node.py 前 10 行 ---")
print(content)

content = my_read("core/node.py", offset=11, limit=5)
print("\n--- node.py 第 11-15 行 ---")
print(content)


print("\n" + "=" * 55)
print("9. Path 操作对照项目代码速查")
print("=" * 55)

print("""
项目代码                        Path 方法
──────────────────────────────────────────────────
read.py:35  file_path.resolve()  → .resolve()
read.py:37  file_path.exists()   → .exists()
read.py:44  .read_text(enc)      → .read_text()
write.py    .write_text(content) → .write_text()
grep.py     .rglob("*.py")       → .rglob()
ls.py       .iterdir()           → .iterdir()
find.py     .rglob("*")          → .rglob()
skill_loader.py:9  .parents[1]   → .parent.parent
skill_loader.py:15 .read_text()  → .read_text()
""")
