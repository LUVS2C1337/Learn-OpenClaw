# Learn-OpenClaw — AI Agent 开发教程

## 项目简介
从零构建自定义 AI Agent 的教程（约 9 小时），用纯 Python 手写框架，不依赖 LangChain。

## 核心架构
- **Node** = 最小处理单元，60 行代码实现（`core/node.py`）
- **Flow** = 按 action 串联 Node 的编排器
- **Workflow = Node + Node**
- **Chatbot = Workflow + Loop**
- **Agent = Chatbot + Tools = Workflow + Loop + Tools**

## 已配置的环境
- **LLM**: DeepSeek (`deepseek-chat`)
- **API Key**: 已写入 `.env` 文件
- **Base URL**: `https://api.deepseek.com/v1`
- **Python**: uv 虚拟环境 `.venv`
- **依赖**: 已通过 `uv sync` 安装

## 关键文件
| 文件 | 说明 |
|---|---|
| `core/node.py` | Node 和 Flow 核心类（~56 行） |
| `core/llm.py` | LLM 调用封装（call_llm / call_llm_simple） |
| `core/skill_loader.py` | Skill 加载器 |
| `examples/workflow/main.py` | 基础 Workflow 示例（搜索→总结） |
| `examples/chatbot/main.py` | 简单对话机器人 |
| `examples/chatbot_with_tools/main.py` | 带工具调用的 Agent（MCP） |
| `tools/` | 内置工具集（search, bash, files 等） |

## 学习元规则（每次学习必经）
1. **当前最没把握的事是什么？** — 识别真正的薄弱点（通常不是表面的"没听懂"，而是"能不能自己改代码"）
2. **当前最大的遗漏是什么？没意识到什么？** — 警惕"消费代码"而非"生产代码"的陷阱，卡住才是真学习

## 运行命令
```bash
# 激活环境
cd D:\CC\Learn-OpenClaw
uv sync

# 运行示例
uv run python examples/workflow/main.py       # Workflow
uv run python examples/chatbot/main.py         # Chatbot
uv run python examples/chatbot_with_tools/main.py  # Agent + Tools

# 运行指定入口（pyproject.toml 已配置）
uv run workflow
uv run chatbot
uv run search
```

## 当前进度
- [x] 配置 DeepSeek API
- [x] 修改 `core/llm.py` 模型名为 `deepseek-chat`
- [x] 测试通过 Workflow 示例
- [x] 理解 Node 核心概念（Node/Flow/>>/- 运算符/action 路由）
- [x] 学习 Chatbot 示例（Chatbot = Workflow + Loop）
- [ ] 学习带工具的 Agent 示例
- [ ] 理解 Tool/MCP/Skill 概念
- [ ] 理解 Memory 机制（工业级方案）
- [ ] 理解 Multi-Agent
