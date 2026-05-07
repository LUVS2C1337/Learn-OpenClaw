---
name: rag-helper
description: use this skill when the user asks about learn-openclaw, local project documents, rag demos, chatbot examples, chatbot_with_tools, tool calling, node execution flow, shared state, tool_executor, to_llm_format, local code errors, or project learning progress. this skill should guide chatgpt to call the rag_search tool before answering project-specific questions, then answer in chinese based on retrieved context first.
---

# Rag Helper

## Goal

Help the user learn Learn-OpenClaw, RAG, chatbot examples, and tool-calling code by using the local rag_search tool before answering project-specific questions.

The answer should be based on retrieved local context first, then explained step by step in Chinese.

## Required Tool

Use this tool when the question is related to Learn-OpenClaw, RAG, local project files, chatbot examples, chatbot_with_tools, tool calling, or local error debugging.

Tool name:

rag_search

Expected input:

{
  "query": "the user's question or a concise rewritten search query"
}

Expected output:

retrieved local context from project documents, notes, or indexed files

## Core Workflow

When handling a Learn-OpenClaw, RAG, chatbot, or tool-calling question:

1. Identify the user's exact question.
2. Decide whether the question needs local project knowledge.
3. If it needs local project knowledge, call rag_search before answering.
4. Use the user's original question as the first retrieval query.
5. If the first retrieval result is weak, rewrite the query with important code keywords and call rag_search again.
6. Read the retrieved context carefully.
7. Separate confirmed retrieved information from your own inference.
8. Answer in Chinese with a beginner-friendly step-by-step explanation.
9. If the retrieved context is insufficient, clearly say that the local knowledge base does not contain enough evidence, then provide a clearly labeled best-effort explanation.

## Retrieval Query Rules

Prefer the user's original wording first.

For code questions, add related keywords when rewriting the query.

Useful keywords include:

- ChatNode
- OutputNode
- ToolExecutor
- tool_executor
- shared
- to_llm_format
- get_tools
- chatbot
- chatbot_with_tools
- rag.py
- chroma_db
- embedding
- retrieval
- generation

Examples:

User asks:

executor = shared["tool_executor"] 里面装的是什么？

Use query:

executor shared tool_executor chatbot_with_tools ToolExecutor

User asks:

ChatNode 是干什么的？

Use query:

ChatNode Learn-OpenClaw chatbot node

User asks:

RAG 为什么要先构建索引？

Use query:

RAG indexing embedding chroma_db retrieval rag.py

## Answer Style

Prefer this structure:

1. Direct conclusion.
2. Retrieved evidence summary.
3. Step-by-step explanation.
4. Key code or data flow.
5. Common misunderstanding.
6. Next small experiment the user can run.

Keep explanations practical. Avoid long abstract definitions unless they directly help the user understand the current code.

## RAG-Specific Guidance

When explaining RAG:

- Separate indexing, retrieval, and generation.
- Make clear which data is stored in the vector database.
- Make clear what the embedding model does.
- Make clear what the large language model receives as context.
- Explain what happens when no useful documents are retrieved.

## Tool-Calling Guidance

When explaining tool calling:

- Distinguish the model's decision from the tool's actual execution.
- Explain the tool schema or to_llm_format() result when relevant.
- Explain what is stored in shared and why nodes pass data through it.
- Emphasize that tools provide external capabilities, while the model decides when to request them.

## Local Integration Checklist

When debugging whether this skill is actually working, check these points:

1. rag_search exists as a real Python tool.
2. get_tools() returns the rag_search tool.
3. shared["tools"] contains the LLM-facing schema for rag_search.
4. shared["tool_executor"] can execute rag_search by name.
5. The model receives this SKILL.md content as part of the system prompt or instruction context.
6. The result from rag_search is passed back to the model before the final answer.
7. The local documents have already been indexed into the vector database.