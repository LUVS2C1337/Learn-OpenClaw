import json
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from tools import ToolExecutor


class MCPClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def list_tools(self):
        url = f"{self.base_url}/list_tools"

        with urlopen(url) as response:
            data = response.read().decode("utf-8")

        return json.loads(data)

    def call_tool(self, name: str, arguments: dict):
        url = f"{self.base_url}/call_tool"

        payload = {
            "name": name,
            "arguments": arguments,
        }

        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")

        request = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        with urlopen(request) as response:
            data = response.read().decode("utf-8")

        result = json.loads(data)

        if "error" in result:
            raise RuntimeError(result["error"])

        return result["result"]


@dataclass
class MCPToolResult:
    tool_call_id: str | None
    name: str
    content: str

    def to_message(self):
        message = {
            "role": "tool",
            "content": self.content,
        }

        if self.tool_call_id:
            message["tool_call_id"] = self.tool_call_id
        else:
            message["name"] = self.name

        return message


class MCPToolExecutor:
    def __init__(self, client: MCPClient):
        self.client = client
        self.parser = ToolExecutor()

    def parse_tool_calls(self, response):
        return self.parser.parse_tool_calls(response)

    def execute_all(self, tool_calls):
        results = []

        for tc in tool_calls:
            tool_name = tc.name
            arguments = tc.arguments

            if isinstance(arguments, str):
                arguments = json.loads(arguments)

            print(f"[MCP Client] 远程调用: {tool_name}({arguments})")

            result = self.client.call_tool(tool_name, arguments)

            if not isinstance(result, str):
                result = json.dumps(result, ensure_ascii=False, indent=2)

            print(f"[MCP Client] 远程结果: {result}")

            tool_call_id = getattr(tc, "id", None)
            if tool_call_id is None:
                tool_call_id = getattr(tc, "tool_call_id", None)

            results.append(
                MCPToolResult(
                    tool_call_id=tool_call_id,
                    name=tool_name,
                    content=result,
                )
            )

        return results