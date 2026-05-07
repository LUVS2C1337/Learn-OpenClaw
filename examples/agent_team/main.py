from __future__ import annotations

import sys
from pathlib import Path


# 把项目根目录加入 Python import 路径
# 当前文件路径: examples/agent_team/main.py
# parents[2] 就是 Learn-OpenClaw 项目根目录
ROOT_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT_DIR))


from core.llm import call_llm
from team import AgentTeam


class LLMAdapter:
    """
    把 core.llm.call_llm 适配成 llm.chat(messages) 的形式。

    因为我们前面写的 Agent 里调用的是:
        self.llm.chat(messages)

    但 Learn-OpenClaw 里的实际 LLM 函数是:
        call_llm(messages)
    """

    def chat(self, messages):
        result = call_llm(messages)

        # call_llm 返回的是一个 dict:
        # {
        #   "role": "assistant",
        #   "content": "...",
        #   ...
        # }
        return result.get("content", "")


def main():
    llm = LLMAdapter()
    team = AgentTeam(llm)

    print("Agent Team Demo")
    print("输入 q / quit / exit 退出")
    print("-" * 40)

    while True:
        user_input = input("\n请输入任务：").strip()

        if user_input.lower() in {"q", "quit", "exit"}:
            print("已退出。")
            break

        if not user_input:
            continue

        print("\n[AgentTeam] 正在处理任务...\n")

        try:
            result = team.run(user_input)
        except Exception as e:
            print("运行出错：", e)
            continue

        print("\n最终结果：")
        print(result)


if __name__ == "__main__":
    main()