"""Tests for core/llm.py — LLM call helpers."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.llm import call_llm_simple, call_llm


def test_call_llm_simple_returns_string():
    """call_llm_simple should return a non-empty string"""
    result = call_llm_simple("用两个字回答：你好吗？")
    assert isinstance(result, str)
    assert len(result) > 0


def test_call_llm_returns_dict():
    """call_llm should return a dict with role and content"""
    result = call_llm(messages=[{"role": "user", "content": "用两个字回答：你好吗？"}])
    assert isinstance(result, dict)
    assert "role" in result
    assert result["role"] == "assistant"
    assert "content" in result
    assert len(result["content"]) > 0


def test_call_llm_with_system_prompt():
    """call_llm should prepend system prompt"""
    result = call_llm(
        messages=[{"role": "user", "content": "说你好"}],
        system_prompt="你是一个友好的助手。只用中文回答。",
    )
    assert isinstance(result, dict)
    assert len(result["content"]) > 0
