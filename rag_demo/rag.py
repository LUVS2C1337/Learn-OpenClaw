import os
from pathlib import Path

import chromadb
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


DOCS_DIR = Path("./docs")
CHROMA_DIR = "./chroma_db"
COLLECTION_NAME = "my_rag_docs"


# Chroma 本地向量数据库
chroma_client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = chroma_client.get_or_create_collection(
    name=COLLECTION_NAME
)


# embedding API 客户端：负责把文字变成向量
embedding_client = OpenAI(
    api_key=os.getenv("EMBEDDING_API_KEY"),
    base_url=os.getenv("EMBEDDING_BASE_URL"),
)


# Kimi 客户端：负责最终回答问题
kimi_client = OpenAI(
    api_key=os.getenv("KIMI_API_KEY"),
    base_url=os.getenv("KIMI_BASE_URL"),
)


def get_embedding(text: str):
    """
    把一段文字转成向量。
    """
    response = embedding_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=text,
    )

    return response.data[0].embedding


def get_embeddings(texts: list[str]):
    """
    批量把多段文字转成向量。
    """
    response = embedding_client.embeddings.create(
        model=os.getenv("EMBEDDING_MODEL"),
        input=texts,
    )

    return [item.embedding for item in response.data]


def load_text_files():
    """
    读取 docs 文件夹里的 txt , md , py 文件。
    支持子文件夹。
    """
    documents = []

    supported_suffixes = [".txt", ".md", ".py"]

    for path in DOCS_DIR.rglob("*"):
        if path.is_dir():
            continue

        if path.suffix.lower() not in supported_suffixes:
            continue

        text = path.read_text(encoding="utf-8", errors="ignore")

        documents.append({
            "source": str(path),
            "text": text,
        })

    return documents


def split_text(text: str, chunk_size: int = 800, overlap: int = 50):
    """
    把长文本切成小块。
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start = start + chunk_size - overlap

    return chunks


def build_index():
    """
    把 docs 里的文档写入 Chroma。
    """
    docs = load_text_files()

    ids = []
    texts = []
    metadatas = []

    for doc_index, doc in enumerate(docs):
        chunks = split_text(doc["text"])

        for chunk_index, chunk in enumerate(chunks):
            chunk_id = f"doc_{doc_index}_chunk_{chunk_index}"

            ids.append(chunk_id)
            texts.append(chunk)
            metadatas.append({
                "source": doc["source"],
                "chunk_index": chunk_index,
            })

    if not texts:
        print("没有读取到文档，请检查 docs 文件夹里有没有 txt 或 md 文件。")
        return

    print(f"开始生成 embedding，共 {len(texts)} 个文本块...")

    embeddings = get_embeddings(texts)

    collection.upsert(
        ids=ids,
        documents=texts,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    print(f"索引构建完成，共写入 {len(texts)} 个文本块。")


def retrieve(question: str, top_k: int = 3):
    """
    根据问题，从 Chroma 中检索相关文本。
    """
    question_embedding = get_embedding(question)

    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=top_k,
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    retrieved = []

    for text, metadata in zip(documents, metadatas):
        retrieved.append({
            "text": text,
            "source": metadata["source"],
        })

    return retrieved


def ask_kimi(question: str, contexts: list[dict]):
    """
    把检索到的资料交给 Kimi 回答。
    """
    context_text = ""

    for i, item in enumerate(contexts):
        context_text += f"\n资料 {i + 1}，来源：{item['source']}\n"
        context_text += item["text"]
        context_text += "\n"

    response = kimi_client.chat.completions.create(
        model=os.getenv("KIMI_MODEL"),
        messages=[
            {
                "role": "system",
                "content": "你是一个严谨的助手。请只根据提供的资料回答问题。资料里没有的信息，不要编造。",
            },
            {
                "role": "user",
                "content": f"""
下面是检索到的资料：

{context_text}

请根据上面的资料回答问题：

{question}
""",
            },
        ],
        temperature=1,
    )

    return response.choices[0].message.content


def rag_ask(question: str):
    contexts = retrieve(question)

    print("\n检索到的资料：")
    for item in contexts:
        print("- 来源：", item["source"])
        print(item["text"][:100], "...")
        print()

    answer = ask_kimi(question, contexts)

    print("\n回答：")
    print(answer)


if __name__ == "__main__":
    choice = input("是否重新构建索引？输入 y 重新构建，直接回车跳过：").strip()

    if choice.lower() == "y":
        build_index()
    else:
        print("跳过索引构建，直接使用已有 Chroma 数据库。")

    while True:
        question = input("\n请输入问题，输入 q 退出：").strip()

        if question.lower() == "q":
            break

        rag_ask(question)