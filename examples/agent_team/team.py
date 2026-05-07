from pathlib import Path
import re
from concurrent.futures import ThreadPoolExecutor

from agents import Agent
from prompts import (
    COORDINATOR_PROMPT,
    CODE_AGENT_PROMPT,
    REVIEW_AGENT_PROMPT,
    TRACE_AGENT_PROMPT,
)


ROOT_DIR = Path(__file__).resolve().parents[2]


class AgentTeam:
    def __init__(self, llm):
        self.coordinator = Agent("CoordinatorAgent", llm, COORDINATOR_PROMPT)
        self.code_agent = Agent("CodeAgent", llm, CODE_AGENT_PROMPT)
        self.trace_agent = Agent("TraceAgent", llm, TRACE_AGENT_PROMPT)
        self.review_agent = Agent("ReviewAgent", llm, REVIEW_AGENT_PROMPT)

    def _guess_target_dir(self, user_input):
        """
        从用户输入里尝试提取 examples/xxx 这种路径。

        例如：
            帮我解释 examples/chatbot_with_tools 是怎么工作的

        会提取出：
            examples/chatbot_with_tools
        """
        match = re.search(r"(examples/[a-zA-Z0-9_\-/]+)", user_input)

        if match:
            return match.group(1).rstrip("，。,. ")

        return None

    def _read_project_files(self, relative_dir, max_chars=20000):
        """
        读取指定目录下的 Python 文件，作为代码上下文提供给 Agent。
        """
        target_dir = ROOT_DIR / relative_dir

        if not target_dir.exists():
            return f"未找到目录：{relative_dir}"

        parts = []
        total_chars = 0

        for path in sorted(target_dir.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue

            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                content = path.read_text(encoding="utf-8", errors="ignore")

            relative_path = path.relative_to(ROOT_DIR)

            block = f"""
文件：{relative_path}

文件内容开始：
{content}
文件内容结束。
"""

            if total_chars + len(block) > max_chars:
                parts.append("\n代码内容较长，后续文件已省略。")
                break

            parts.append(block)
            total_chars += len(block)

        if not parts:
            return f"目录 {relative_dir} 下没有找到 Python 文件。"

        return "\n".join(parts)

    def run(self, user_input):
        # 第一步：ProjectReaderAgent 读取代码上下文
        target_dir = self._guess_target_dir(user_input)

        if target_dir:
            print(f"[ProjectReaderAgent] 正在读取 {target_dir} ...", flush=True)
            code_context = self._read_project_files(target_dir)
            print("[ProjectReaderAgent] 读取完成。", flush=True)
        else:
            code_context = "用户没有指定明确的项目目录。"

        # 第二步：CoordinatorAgent 拆任务
        plan = self.coordinator.run(f"""
你是 CoordinatorAgent。

请把用户任务拆成适合多个 Agent 执行的子任务。

用户任务：
{user_input}

已读取到的项目代码上下文：
{code_context}

请只输出清晰的任务拆分列表。
""")["result"]

        # 第三步：准备两个可以并行执行的 Worker 任务
        # 注意：ReviewAgent 依赖 CodeAgent / TraceAgent 的结果，所以它不能放在这里并行。
        # 这里并行的是两个互不依赖的 Agent：
        #   - CodeAgent：解释代码功能
        #   - TraceAgent：梳理真实执行链路

        code_task = f"""
你是 CodeAgent。

请基于真实项目代码回答用户问题，不要凭空猜测。

用户任务：
{user_input}

CoordinatorAgent 的任务拆分：
{plan}

项目代码上下文：
{code_context}

请详细解释这个功能是怎么工作的。
如果涉及代码流程，请按执行顺序说明。
要求：
1. 只能根据代码上下文回答
2. 不要提代码里没有出现的概念
3. 不确定的地方要明确说“不确定”
"""

        trace_task = f"""
你是 TraceAgent。

请根据项目代码上下文，梳理这个功能的真实执行链路。

用户任务：
{user_input}

CoordinatorAgent 的任务拆分：
{plan}

项目代码上下文：
{code_context}

请输出：
1. 程序入口文件
2. main.py 的执行顺序
3. 用户输入如何进入系统
4. LLM 调用发生在哪里
5. tools 是在哪里加载和执行的
6. 最终结果是如何输出的

要求：
1. 只能根据代码上下文回答
2. 不要提代码里没有出现的概念
3. 不确定的地方要明确说“不确定”
"""

        # 第四步：并行执行 CodeAgent 和 TraceAgent
        print("\n[AgentTeam] 并行启动 CodeAgent 和 TraceAgent ...", flush=True)

        with ThreadPoolExecutor(max_workers=2) as executor:
            code_future = executor.submit(self.code_agent.run, code_task)
            trace_future = executor.submit(self.trace_agent.run, trace_task)

            code_result = code_future.result()
            trace_result = trace_future.result()

        print("[AgentTeam] 并行任务完成。", flush=True)

        # 第五步：ReviewAgent 审查 CodeAgent 和 TraceAgent 的结果
        # ReviewAgent 放在并行阶段之后，因为它需要看到两个 Worker Agent 的输出。
        review_result = self.review_agent.run(f"""
你是 ReviewAgent。

请审查 CodeAgent 和 TraceAgent 的结果是否符合项目代码上下文。

用户任务：
{user_input}

项目代码上下文：
{code_context}

CodeAgent 结果：
{code_result["result"]}

TraceAgent 结果：
{trace_result["result"]}

请指出：
1. CodeAgent 哪些解释准确
2. TraceAgent 哪些执行链路准确
3. 有没有提到代码里不存在的概念
4. 有没有遗漏关键流程
5. 最终答案应该保留哪些内容，删除哪些内容

要求：
1. 只能根据项目代码上下文审查
2. 如果 CodeAgent 或 TraceAgent 提到了代码里没有的概念，必须指出
3. 不要重新发散生成无关内容
""")

        # 第六步：CoordinatorAgent 汇总最终答案
        final_result = self.coordinator.run(f"""
你是 CoordinatorAgent。

请根据 CodeAgent、TraceAgent 和 ReviewAgent 的结果，给用户一个最终答案。

用户原始任务：
{user_input}

项目代码上下文：
{code_context}

CoordinatorAgent 的任务拆分：
{plan}

CodeAgent 结果：
{code_result["result"]}

TraceAgent 结果：
{trace_result["result"]}

ReviewAgent 审查结果：
{review_result["result"]}

要求：
1. 最终答案必须基于代码上下文
2. 不要说没有代码依据的话
3. 不要提代码里没有出现的概念
4. 用中文解释
5. 按真实执行顺序说明
6. 如果 CodeAgent、TraceAgent、ReviewAgent 说法不一致，以代码上下文和 ReviewAgent 审查为准
""")

        return final_result["result"]