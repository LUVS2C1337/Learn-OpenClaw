"""练习三：看懂 Tool 格式 + 模拟 Tool Calling"""

import sys, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from tools.builtins import get_builtin_tools
from tools.executor import ToolExecutor

# 1. 获取工具列表，打印 write 工具的 LLM 格式
tools = get_builtin_tools()
write_tool = tools[1]  # read=0, write=1
print("= write 工具的 LLM 格式 =")
print(json.dumps(write_tool.to_llm_format(), indent=2, ensure_ascii=False))

# 2. 模拟 LLM 调 bash 执行 dir
print("\n= 模拟：LLM 调 bash('dir') =")
executor = ToolExecutor()

fake_response = {
    "role": "assistant",
    "content": "我来执行 dir 命令",
    "tool_calls": [
        {
            "id": "call_001",
            "type": "function",
            "function": {
                "name": "bash",
                "arguments": '{"command": "dir"}'
            }
        }
    ]
}

tc = executor.parse_tool_calls(fake_response)
results = executor.execute_all(tc)

for t, r in zip(tc, results):
    print(f"  调用: {t.name}({t.arguments})")
    print(f"  结果:\n{r.content[:300]}")
