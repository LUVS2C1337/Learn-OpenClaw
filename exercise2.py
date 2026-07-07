"""练习二：计数器机器人"""

import sys
from pathlib import Path
from typing import Any, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from core.llm import call_llm
from core.node import Node, Flow, shared

SYSTEM_PROMPT = "你是一个友好的对话助手，请回答用户的问题。"


class ChatNode(Node):
    """对话节点：每轮计数 + 调用 LLM"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        messages = shared["messages"]
        shared["turn"] += 1
        turn = shared["turn"]

        # 在消息开头加上轮次标记
        response = call_llm(messages=messages, system_prompt=SYSTEM_PROMPT)
        content = response.get("content", "")
        response["content"] = f"[第 {turn} 轮]\n{content}"

        messages.append(response)
        return "output", response


class OutputNode(Node):
    """输出节点：显示助手回复"""

    def exec(self, payload: Any) -> Tuple[str, Any]:
        content = payload.get("content", "")
        print(f"\n🤖 Assistant: {content}\n")
        return "default", None


def main():
    shared.clear()
    shared["messages"] = []
    shared["turn"] = 0

    chat = ChatNode()
    output = OutputNode()
    chat - "output" >> output

    print("=" * 60)
    print("🤖 计数器机器人")
    print("=" * 60)
    print("输入 'quit' 或 'exit' 退出\n")

    while True:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            print("\n再见！")
            break
        if not user_input:
            continue

        shared["messages"].append({"role": "user", "content": user_input})
        flow = Flow(chat)
        flow.run(None)


if __name__ == "__main__":
    main()
