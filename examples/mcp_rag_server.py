import json
import sys
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


from tools import get_tools


ALLOWED_TOOLS = {"rag_search"}


def get_tool_name(tool):
    if hasattr(tool, "name"):
        return tool.name

    if hasattr(tool, "to_llm_format"):
        schema = tool.to_llm_format()
        if "function" in schema:
            return schema["function"]["name"]
        return schema.get("name")

    return None


def load_mcp_tools():
    tools = get_tools()
    tool_map = {}

    for tool in tools:
        name = get_tool_name(tool)
        if name in ALLOWED_TOOLS:
            tool_map[name] = tool

    return tool_map


MCP_TOOLS = load_mcp_tools()


def tool_to_schema(tool):
    if hasattr(tool, "to_llm_format"):
        return tool.to_llm_format()

    name = get_tool_name(tool)

    return {
        "type": "function",
        "function": {
            "name": name,
            "description": "远程工具",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }


def call_tool_object(tool, arguments):
    if hasattr(tool, "run"):
        try:
            return tool.run(**arguments)
        except TypeError:
            return tool.run(arguments)

    if hasattr(tool, "execute"):
        try:
            return tool.execute(**arguments)
        except TypeError:
            return tool.execute(arguments)

    if hasattr(tool, "func"):
        return tool.func(**arguments)

    if callable(tool):
        return tool(**arguments)

    raise RuntimeError(f"工具对象不可执行: {tool}")


class MCPHandler(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/list_tools":
            schemas = [tool_to_schema(tool) for tool in MCP_TOOLS.values()]
            self._send_json(schemas)
            return

        self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        if self.path != "/call_tool":
            self._send_json({"error": "not found"}, status=404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(length).decode("utf-8")

        try:
            payload = json.loads(raw_body)

            tool_name = payload["name"]
            arguments = payload.get("arguments", {})

            if tool_name not in MCP_TOOLS:
                self._send_json(
                    {"error": f"未知工具或未开放工具: {tool_name}"},
                    status=400
                )
                return

            print(f"[MCP Server] 调用工具: {tool_name}({arguments})")

            result = call_tool_object(MCP_TOOLS[tool_name], arguments)

            print(f"[MCP Server] 工具结果: {result}")

            self._send_json({
                "name": tool_name,
                "result": result
            })

        except Exception as e:
            self._send_json({"error": str(e)}, status=500)


def main():
    host = "127.0.0.1"
    port = 8000

    print("=" * 60)
    print("MCP RAG Server")
    print("=" * 60)
    print(f"服务地址: http://{host}:{port}")
    print(f"开放工具: {', '.join(MCP_TOOLS.keys())}")
    print("接口:")
    print("  GET  /list_tools")
    print("  POST /call_tool")
    print("=" * 60)

    server = HTTPServer((host, port), MCPHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()