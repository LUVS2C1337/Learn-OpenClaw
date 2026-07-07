"""演示：Agent = Chatbot + Tools 的完整流程"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tools.builtins import get_builtin_tools, Tool
from tools.executor import ToolExecutor

# 1. 获取内置工具（ls, read, grep 等 9 个）
tools = get_builtin_tools()
print(f"= 可用工具: {len(tools)} 个 =")
for t in tools:
    print(f"  - {t.name}: {t.description[:40]}...")

# 2. 工具长什么样（给 LLM 看的格式）
print(f"\n= Tool 的 LLM 格式（示例：ls）= ")
import json
print(json.dumps(tools[6].to_llm_format(), indent=2, ensure_ascii=False))

# 3. 模拟 LLM 调工具
print(f"\n= 模拟：LLM 决定调 ls 和 bash =")
executor = ToolExecutor()

fake_llm_response = {
    "role": "assistant",
    "content": "我来查看目录结构",
    "tool_calls": [
        {
            "id": "call_001",
            "type": "function",
            "function": {
                "name": "ls",
                "arguments": '{"path": "."}'
            }
        },
        {
            "id": "call_002",
            "type": "function",
            "function": {
                "name": "bash",
                "arguments": '{"command": "echo hello"}'
            }
        }
    ]
}

tool_calls = executor.parse_tool_calls(fake_llm_response)
results = executor.execute_all(tool_calls)

for tc, r in zip(tool_calls, results):
    print(f"\n  调用: {tc.name}{tc.arguments}")
    print(f"  结果: {r.content[:80]}")

# 4. 工具结果 → 放回对话历史
print(f"\n= 工具结果格式（追加到 messages）= ")
for r in results:
    msg = r.to_message()
    print(f"  role: {msg['role']}, tool_call_id: {msg['tool_call_id']}")
    print(f"  content: {msg['content'][:60]}...")
