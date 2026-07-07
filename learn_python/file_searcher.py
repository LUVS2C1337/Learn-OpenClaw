"""实战：文件搜索工具（File Searcher）
功能：搜索文件夹里的文件内容，支持按文件名匹配和按内容匹配。
    学完后你能看懂 tools/builtins/ 里的 read.py、write.py、grep.py、find.py
"""

import sys
from pathlib import Path
import fnmatch


# ==========================================
# FileSearcher 类（核心逻辑）
# ==========================================

class FileSearcher:
    """文件搜索工具
    对应项目里的 grep.py（按内容搜索）和 find.py（按名字搜索）
    """

    def __init__(self, root_dir="."):
        self.root = Path(root_dir).resolve()
        if not self.root.exists():
            raise FileNotFoundError(f"目录不存在: {self.root}")
        if not self.root.is_dir():
            raise NotADirectoryError(f"不是目录: {self.root}")
        # 默认排除的目录
        self.exclude_dirs = {".venv", "__pycache__", ".git", ".mypy_cache", ".pytest_cache", "node_modules"}

    def _should_skip(self, path: Path) -> bool:
        """检查路径是否应该被跳过"""
        for part in path.parts:
            if part in self.exclude_dirs:
                return True
        return False

    def find_by_name(self, pattern: str):
        """按文件名搜索（支持通配符 *.py, *test* 等）
        对应项目里的 find.py
        """
        results = []
        for path in self.root.rglob("*"):
            if self._should_skip(path):
                continue
            if path.is_file() and fnmatch.fnmatch(path.name, pattern):
                results.append(path)
        return results

    def grep(self, keyword: str, glob_pattern: str = "*.py"):
        """按文件内容搜索关键词
        对应项目里的 grep.py
        """
        results = []
        for path in self.root.rglob(glob_pattern):
            if self._should_skip(path):
                continue
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if keyword in line:
                    results.append((path, i, line.strip()))
        return results

    def tree(self):
        """打印目录树
        对应项目里的 ls.py
        """
        lines = []
        self._tree_walk(self.root, lines, "")
        return "\n".join(lines)

    def _tree_walk(self, path: Path, lines: list, prefix: str):
        """递归打印目录树"""
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        for i, entry in enumerate(entries):
            is_last = (i == len(entries) - 1)
            connector = "└── " if is_last else "├── "
            lines.append(f"{prefix}{connector}{entry.name}")
            if entry.is_dir():
                next_prefix = prefix + ("    " if is_last else "│   ")
                self._tree_walk(entry, lines, next_prefix)


# ==========================================
# 工具函数（用于 demo 模式）
# ==========================================

def _demo():
    """无参数时运行演示"""
    searcher = FileSearcher(".")

    # 演示 Path 操作
    print("Path 操作演示:")
    current = Path(__file__)
    print(f"  当前文件:      {current}")
    print(f"  文件名:        {current.name}")
    print(f"  父目录:        {current.parent}")
    print(f"  父父目录:      {current.parent.parent}")
    print()

    # 演示：按文件名搜索 .md 文件
    print("1. 按文件名搜索 *.md:")
    for f in searcher.find_by_name("*.md")[:10]:
        print(f"  {f.relative_to(searcher.root)}")
    print()

    # 演示：按内容搜索 "class Node"
    print("2. 按内容搜索 'class Node':")
    matches = searcher.grep("class Node", "*.py")
    for path, ln, text in matches[:5]:
        print(f"  {path.relative_to(searcher.root)}:{ln}  {text[:60]}")
    if len(matches) > 5:
        print(f"  ... 共 {len(matches)} 条")
    print()

    # 演示：目录树（前2层）
    print("3. 项目目录树（前2层）:")
    for line in searcher.tree().split("\n")[:25]:
        print(f"  {line}")
    print(f"  ...")


# ==========================================
# if __name__ — 根据参数决定做什么
# ==========================================

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        # CLI 模式
        cmd = sys.argv[1]
        searcher = FileSearcher(".")

        if cmd == "tree":
            print(searcher.tree())
        elif cmd == "find" and len(sys.argv) >= 3:
            results = searcher.find_by_name(sys.argv[2])
            for r in results[:30]:
                print(f"  {r.relative_to(searcher.root)}")
        elif cmd == "grep" and len(sys.argv) >= 3:
            results = searcher.grep(sys.argv[2], "*.py")
            for path, ln, text in results[:20]:
                print(f"  {path.relative_to(searcher.root)}:{ln}  {text[:60]}")
        else:
            print(f"用法: python {sys.argv[0]} [tree|find|grep] [参数]")
    else:
        # Demo 模式
        _demo()
