import json
import os
import sys
from pathlib import Path

import requests

GITHUB_REPO = "KevinRorzeDev/ClaudeMCPTests"
INSTALL_DIR = Path(os.environ["LOCALAPPDATA"]) / "BOMCheck"
CLAUDE_CONFIG = Path(os.environ["APPDATA"]) / "Claude" / "claude_desktop_config.json"
API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"


def get_headers():
    token = os.environ.get("GITHUB_TOKEN")
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch_latest_release():
    print("Checking GitHub for latest release...")
    response = requests.get(API_URL, headers=get_headers(), timeout=10)
    response.raise_for_status()
    release = response.json()
    print(f"Found release: {release['tag_name']}")
    return release


def download_assets(release):
    INSTALL_DIR.mkdir(parents=True, exist_ok=True)
    headers = {**get_headers(), "Accept": "application/octet-stream"}
    for asset in release["assets"]:
        name = asset["name"]
        asset_id = asset["id"]
        dest = INSTALL_DIR / name
        print(f"Downloading {name}...")
        url = f"https://api.github.com/repos/{GITHUB_REPO}/releases/assets/{asset_id}"
        response = requests.get(url, headers=headers, timeout=60, allow_redirects=True)
        response.raise_for_status()
        dest.write_bytes(response.content)
        print(f"  Saved to {dest}")


def write_claude_config():
    server_exe = INSTALL_DIR / "server.exe"

    config = {}
    if CLAUDE_CONFIG.exists():
        config = json.loads(CLAUDE_CONFIG.read_text(encoding="utf-8"))

    config.setdefault("mcpServers", {})
    config["mcpServers"]["bom-check"] = {
        "command": str(server_exe),
        "args": [],
    }

    CLAUDE_CONFIG.write_text(json.dumps(config, indent=2), encoding="utf-8")
    print(f"Claude Desktop config updated: {CLAUDE_CONFIG}")


def main():
    release = fetch_latest_release()
    download_assets(release)
    write_claude_config()
    print("\nInstallation complete. Restart Claude Desktop to activate the tool.")


if __name__ == "__main__":
    main()
