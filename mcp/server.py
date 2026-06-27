import asyncio
import subprocess
import sys
from pathlib import Path
from fastmcp import FastMCP

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

mcp = FastMCP("BOM Check")

EXE_PATH = Path(__file__).parent.parent / "dist" / "bom_check.exe"

_CREATE_NO_WINDOW = 0x08000000


@mcp.tool()
def get_secret_code(part_number: str) -> str:
    """Run bom_check.exe with a part number and return the unique code it generates."""
    result = subprocess.run(
        [str(EXE_PATH), part_number],
        stdin=subprocess.DEVNULL,
        capture_output=True,
        text=True,
        timeout=10,
        creationflags=_CREATE_NO_WINDOW,
    )
    if result.returncode != 0:
        raise RuntimeError(f"bom_check.exe failed: {result.stderr.strip()}")
    return result.stdout.strip()


if __name__ == "__main__":
    mcp.run(transport="stdio")
