# Learn-OpenClaw — Lightweight AI Agent Framework

A minimalist agent framework built from scratch in Python (~500 lines core), without LangChain or other heavy frameworks. Demonstrates the complete architecture of an AI agent: **Node → Workflow → Chatbot → Agent with Tools → RAG → Multi-Agent**.

## Architecture

```
         ┌─────────────────────────────────────────┐
         │            Agent = Workflow + Loop + Tools          │
         └─────────────────────────────────────────┘
                          │
         ┌────────────────┴────────────────┐
         │                                 │
         ▼                                 ▼
   ┌──────────┐                     ┌──────────────┐
   │   Node   │                     │    Tools     │
   │  (core)  │                     │  (9 built-in) │
   └────┬─────┘                     └──────┬───────┘
        │                                  │
        ▼                                  ▼
   ┌──────────┐                     ┌──────────────┐
   │  Flow    │                     │   Tool / MCP │
   │ (runner) │                     │   / Skill    │
   └────┬─────┘                     └──────┬───────┘
        │                                  │
        ▼                                  ▼
   ┌──────────┐                     ┌──────────────┐
   │ Chatbot  │                     │  RAG (ChromaDB)│
   │  + Loop  │                     │ + Embedding API│
   └────┬─────┘                     └──────┬───────┘
        │                                  │
        └──────────────┬───────────────────┘
                       ▼
              ┌────────────────┐
              │  Multi-Agent   │
              │  (Agent Team)  │
              └────────────────┘
```

## Project Structure

```
Learn-OpenClaw/
├── core/                    # Agent kernel
│   ├── node.py             # Node + Flow (~56 lines)
│   ├── llm.py              # Unified LLM interface (DeepSeek)
│   └── skill_loader.py     # Skill loading system
├── examples/
│   ├── workflow/            # Linear workflow demo
│   ├── chatbot/             # Conversational agent
│   ├── chatbot_with_tools/  # Agent with Tool Calling + MCP
│   ├── agent_team/          # Multi-agent parallel execution
│   └── mcp_rag_server.py    # MCP server with RAG
├── tools/
│   ├── builtins/            # 9 built-in tools (read, write, bash, ls, grep, find, edit, search, rag_search)
│   ├── executor.py          # Tool call parser and executor
│   ├── mcp/                 # MCP protocol client/server
│   └── skills/              # Skill-based tool loading
├── rag_demo/                # RAG with ChromaDB + Embedding API
│   ├── rag.py              # Build index → Retrieve → Answer
│   └── docs/                # Project documents as knowledge base
├── tests/                   # Unit tests
├── app.py                   # Web demo (Streamlit)
├── Dockerfile               # Container deployment
└── docker-compose.yml       # One-click start
```

## Quick Start

```bash
# Setup
cd Learn-OpenClaw
uv sync

# Run the examples
uv run workflow          # Workflow: Query → Search → Summarize
uv run chatbot           # Chatbot with conversation memory
uv run python examples/agent_team/main.py    # Multi-agent team

# Web demo
uv run streamlit run app.py

# Tests
uv run pytest
```

## Core Concepts

| Concept | Description |
|---|---|
| **Node** | Smallest unit — `exec(payload) → (action, new_payload)`, ~60 lines |
| **Flow** | Orchestrator — routes between nodes by action, 4-line loop |
| **Tool Calling** | LLM returns `tool_calls` → execute → feed result back |
| **MCP** | Remote tool protocol (Anthropic standard) |
| **RAG** | ChromaDB + Embedding → semantic document retrieval |
| **Multi-Agent** | Coordinator/CodeAgent/TraceAgent/ReviewAgent parallel pipeline |

## Why This Project Stands Out

- **No framework dependency**: Pure Python, ~500 lines core — full understanding of each component
- **Minimalist design**: The author advocates that agents only need 4 commands: read, write, edit, bash
- **Full-stack coverage**: From `Node` primitives to `Multi-Agent Teams`, including RAG and MCP protocol
- **Interview-ready**: Tests, Docker, Web demo included

## Tech Stack

`Python 3.13+` `uv` `DeepSeek` `ChromaDB` `Streamlit` `Docker` `pytest`
