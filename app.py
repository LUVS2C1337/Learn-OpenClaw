"""
Learn-OpenClaw Web Demo

Run with: uv run streamlit run app.py
"""

import sys, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from core.node import Node, Flow, shared
from core.llm import call_llm

SYSTEM_PROMPT = "你是一个友好的对话助手。请用中文回答。"

class ChatNode(Node):
    def exec(self, payload):
        messages = shared["messages"]
        response = call_llm(messages=messages, system_prompt=SYSTEM_PROMPT)
        messages.append(response)
        return "output", response

class OutputNode(Node):
    def exec(self, payload):
        return "default", payload.get("content", "")

# Page config
st.set_page_config(
    page_title="Learn-OpenClaw Agent",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Learn-OpenClaw Agent Demo")
st.markdown("A lightweight AI agent framework — talk to the LLM below.")

# Sidebar with info
with st.sidebar:
    st.header("About")
    st.markdown("""
    **Learn-OpenClaw** is a minimalist agent framework built from scratch in Python.

    **Current demo:** Chatbot with conversation memory (Node + Flow + LLM)

    **Architecture:**
    1. `Node` — smallest processing unit
    2. `Flow` — orchestrator that chains nodes
    3. `Chatbot = Flow + Loop`
    4. `Agent = Chatbot + Tools`
    """)

    st.divider()
    st.caption(f"LLM: DeepSeek")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.shared = shared

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message here..."):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)

    # Run the agent
    shared.clear()
    shared["messages"] = [{"role": "user", "content": prompt}]
    # Also load history
    for m in st.session_state.messages:
        shared["messages"].insert(0, m)

    chat = ChatNode()
    output = OutputNode()
    chat - "output" >> output

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                flow = Flow(chat)
                action, result = flow.run(None)
                st.markdown(result)
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.session_state.messages.append({"role": "assistant", "content": result})
            except Exception as e:
                st.error(f"Error: {e}")
