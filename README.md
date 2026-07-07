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

## Interview Highlights

This project demonstrates the following engineering and architectural capabilities:

### System Design
- **Agent architecture from primitives**: Designed a composable `Node → Flow` pipeline where each `Node.exec(payload)` returns `(action, next_payload)` — enabling dynamic routing without a central state machine. This is the same pattern used by LangGraph, but implemented in ~60 lines.
- **Multi-agent orchestration**: Implemented a parallel agent team with `Coordinator → [CodeAgent, TraceAgent] → ReviewAgent → Coordinator` pipeline, using `ThreadPoolExecutor` for parallel sub-agent execution.
- **RAG pipeline**: Built a complete retrieval-augmented generation system with ChromaDB vector store + external embedding API, supporting document chunking, semantic search, and context-grounded LLM response generation.

### Engineering Practices
- **Test-driven development**: 38 pytest tests covering core abstractions (Node, Flow, ToolCall, ToolExecutor), edge cases (retry logic, malformed JSON, missing keys), and LLM integration.
- **Docker containerization**: Multi-stage Dockerfile + `docker-compose.yml` for one-click deployment — reproducible, portable, production-ready.
- **Interactive demo**: Streamlit web application demonstrating the agent in a chat interface — low-friction for non-technical stakeholders.

### Technical Decisions
- **Why ChromaDB over pgvector/Milvus**: Development velocity — ChromaDB's embedded mode eliminates the need for a separate database server during prototyping, while maintaining compatibility with production-grade vector stores.
- **Why minimal tools**: Vercel reported removing 80% of their agent's tools improved text-to-SQL accuracy from 80% to 100% (source). This project follows the same principle: only 4 commands (read, write, edit, bash) are genuinely necessary for a coding agent.
- **MCP over custom tool protocol**: Adopted Anthropic's Model Context Protocol for remote tool interoperability, rather than building a proprietary protocol.

### Topics for Interview Discussion

| Topic | What you can discuss |
|---|---|
| **Agent architecture** | Node + Flow design, action-based routing, retry mechanism |
| **Tool calling** | LLM function calling, tool schema design, result feedback loop |
| **RAG** | Chunking strategies, embedding vs generative models, vector search |
| **Multi-agent** | Parallel execution, context isolation, agent team topology |
| **MCP protocol** | Remote vs local tools, progressive loading, token optimization |
| **Production considerations** | Docker deployment, test coverage, error handling, config management |

## Tech Stack

`Python 3.13+` `uv` `DeepSeek` `ChromaDB` `Streamlit` `Docker` `pytest`
