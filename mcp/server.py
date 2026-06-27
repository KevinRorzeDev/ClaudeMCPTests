import json
import subprocess
import sys
from pathlib import Path

EXE_PATH = Path(sys.executable).parent / "bom_check.exe"

_CREATE_NO_WINDOW = 0x08000000

TOOLS = [
    {
        "name": "get_secret_code",
        "description": "Run bom_check.exe with a part number and return the unique code it generates.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "part_number": {"type": "string", "description": "The part number to look up."}
            },
            "required": ["part_number"],
        },
    }
]


def call_tool(name, arguments):
    if name == "get_secret_code":
        part_number = arguments.get("part_number", "")
        result = subprocess.run(
            [str(EXE_PATH), part_number],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=10,
            creationflags=_CREATE_NO_WINDOW,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip())
        return result.stdout.strip()
    raise ValueError(f"Unknown tool: {name}")


def send(obj):
    sys.stdout.write(json.dumps(obj) + "\n")
    sys.stdout.flush()


def handle(msg):
    method = msg.get("method")
    msg_id = msg.get("id")

    if method == "initialize":
        send({
            "jsonrpc": "2.0", "id": msg_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "BOM Check", "version": "0.1.0"},
            },
        })

    elif method == "notifications/initialized":
        pass

    elif method == "tools/list":
        send({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS}})

    elif method == "tools/call":
        params = msg.get("params", {})
        try:
            output = call_tool(params.get("name"), params.get("arguments", {}))
            send({
                "jsonrpc": "2.0", "id": msg_id,
                "result": {"content": [{"type": "text", "text": output}], "isError": False},
            })
        except Exception as e:
            send({
                "jsonrpc": "2.0", "id": msg_id,
                "result": {"content": [{"type": "text", "text": str(e)}], "isError": True},
            })

    elif msg_id is not None:
        send({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": "Method not found"}})


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
            handle(msg)
        except json.JSONDecodeError:
            pass


if __name__ == "__main__":
    main()
