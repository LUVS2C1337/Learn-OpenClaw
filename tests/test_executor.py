"""Tests for tools/executor.py — ToolCall, ToolResult, ToolExecutor."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from tools.executor import ToolCall, ToolResult, ToolExecutor


class TestToolCall:
    """Test ToolCall dataclass and from_openai_item"""

    def test_create_tool_call(self):
        tc = ToolCall(id="call_1", name="ls", arguments={"path": "."})
        assert tc.id == "call_1"
        assert tc.name == "ls"
        assert tc.arguments == {"path": "."}

    def test_from_openai_item_with_string_args(self):
        item = {
            "id": "call_abc",
            "type": "function",
            "function": {
                "name": "read",
                "arguments": '{"path": "test.txt"}'
            }
        }
        tc = ToolCall.from_openai_item(item)
        assert tc.name == "read"
        assert tc.arguments == {"path": "test.txt"}

    def test_from_openai_item_with_dict_args(self):
        item = {
            "id": "call_xyz",
            "function": {
                "name": "bash",
                "arguments": {"command": "pwd"}
            }
        }
        tc = ToolCall.from_openai_item(item)
        assert tc.name == "bash"
        assert tc.arguments == {"command": "pwd"}

    def test_from_openai_with_missing_function(self):
        item = {"id": "call_001"}
        tc = ToolCall.from_openai_item(item)
        assert tc.name == ""
        assert tc.arguments == {}

    def test_from_openai_with_invalid_json(self):
        item = {
            "id": "call_002",
            "function": {
                "name": "ls",
                "arguments": "not valid json{{{"
            }
        }
        tc = ToolCall.from_openai_item(item)
        assert tc.arguments == {}

    def test_from_openai_with_non_dict_args(self):
        item = {
            "id": "call_003",
            "function": {
                "name": "ls",
                "arguments": 123
            }
        }
        tc = ToolCall.from_openai_item(item)
        assert tc.arguments == {}


class TestToolResult:
    """Test ToolResult dataclass"""

    def test_create_result(self):
        r = ToolResult(tool_call_id="call_1", content="done")
        assert r.content == "done"
        assert r.is_error is False

    def test_create_error_result(self):
        r = ToolResult(tool_call_id="call_1", content="error msg", is_error=True)
        assert r.is_error is True

    def test_to_message(self):
        r = ToolResult(tool_call_id="call_001", content="hello")
        msg = r.to_message()
        assert msg["role"] == "tool"
        assert msg["tool_call_id"] == "call_001"
        assert msg["content"] == "hello"


class TestToolExecutor:
    """Test ToolExecutor"""

    def test_parse_tool_calls_empty(self):
        executor = ToolExecutor()
        result = executor.parse_tool_calls({"role": "assistant", "content": "hi"})
        assert result == []

    def test_parse_tool_calls_with_data(self):
        executor = ToolExecutor()
        msg = {
            "role": "assistant",
            "content": "let me check",
            "tool_calls": [
                {
                    "id": "call_1",
                    "function": {"name": "ls", "arguments": '{"path": "."}'}
                }
            ]
        }
        calls = executor.parse_tool_calls(msg)
        assert len(calls) == 1
        assert calls[0].name == "ls"

    def test_execute_unknown_tool_returns_error(self):
        executor = ToolExecutor()
        tc = ToolCall(id="call_1", name="nonexistent_tool", arguments={})
        result = executor.execute(tc)
        assert result.is_error is True
        assert "not found" in result.content

    def test_execute_ls_returns_content(self):
        """ls should return directory listing"""
        executor = ToolExecutor()
        tc = ToolCall(id="call_1", name="ls", arguments={"path": "."})
        result = executor.execute(tc)
        assert result.is_error is False
        assert "core" in result.content  # core dir should be listed

    def test_execute_all_returns_list(self):
        executor = ToolExecutor()
        calls = [
            ToolCall(id="c1", name="ls", arguments={"path": "."}),
            ToolCall(id="c2", name="unknown", arguments={}),
        ]
        results = executor.execute_all(calls)
        assert len(results) == 2
        assert results[0].is_error is False
        assert results[1].is_error is True
