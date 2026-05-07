from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import chromadb
from dotenv import load_dotenv
from openai import OpenAI


# 当前文件位置：
# Learn-OpenClaw/tools/builtins/rag_search.py
#
# parents[2] 就是 Learn-OpenClaw 项目根目录
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# 你的 RAG 数据库在 rag_demo 里
RAG_DIR = PROJECT_ROOT / "rag_demo"
CHROMA_DIR = RAG_DIR / "chroma_db"

# 读取 rag_demo/.env
load_dotenv(RAG_DIR / ".env")


# 这个名字必须和你 rag.py 里用的 COLLECTION_NAME 一致
COLLECTION_NAME = os.getenv("RAG_COLLECTION_NAME", "my_rag_docs")


embedding_client = OpenAI(
    api_key=os.getenv("EMBEDDING_API_KEY"),
    base_url=os.getenv("EMBEDDING_BASE_URL"),
)

chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
collection = chroma_client.get_or_create_collection(name=COLLECTION_NAME)


def _get_embedding(text: str) -> list[float]:
    response = embedding_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text,
    )

    return response.data[0].embedding


def rag_search(query: str, top_k: int = 4) -> str:
    """
    Search local RAG knowledge base.

    这个工具只负责：
    1. 把问题转成 embedding
    2. 去 Chroma 里检索相关资料
    3. 返回资料文本

    它不负责调用 Kimi 生成最终回答。
    最终回答交给 chatbot_with_tools 里的 ChatNode。
    """
    query = query.strip()

    if not query:
        return "Error: query 不能为空。"

    try:
        top_k = int(top_k)
    except Exception:
        top_k = 4

    top_k = max(1, min(top_k, 8))

    try:
        count = collection.count()
    except Exception as exc:
        return f"Error: 无法读取 Chroma 数据库：{exc}"

    if count == 0:
        return (
            "Error: RAG 知识库为空。"
            "请先进入 rag_demo 目录，运行 python rag.py，并选择 y 重新构建索引。"
        )

    try:
        query_embedding = _get_embedding(query)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
        )
    except Exception as exc:
        return f"Error: RAG 检索失败：{exc}"

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]

    if not documents:
        return "没有在 RAG 知识库中检索到相关资料。"

    parts: list[str] = []

    for index, text in enumerate(documents):
        metadata: dict[str, Any] = metadatas[index] if index < len(metadatas) else {}
        distance = distances[index] if index < len(distances) else None

        source = metadata.get("source", "unknown")
        chunk_index = metadata.get("chunk_index", "unknown")

        header = f"资料 {index + 1}\n来源：{source}\nchunk_index：{chunk_index}"

        if distance is not None:
            header += f"\ndistance：{distance}"

        parts.append(f"{header}\n内容：\n{text}")

    return "\n\n---\n\n".join(parts)