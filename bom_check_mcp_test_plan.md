# BOM Check MCP — Proof of Concept Test Plan

## Overview

This plan validates the full delivery pipeline for the BOM Check MCP tooling before any real BOM logic is written. Each phase proves one layer of the stack. Phases are sequential — do not move to the next phase until the current one passes.

---

## Phase 1 — Python script and GitHub repo

**Goal:** Establish the repo structure and confirm a working baseline script.

- Create a new GitHub repository that will eventually track all MCP binaries, scripts, and libraries
- Write a Python script that prints a unique code each time it is run (e.g. a timestamp combined with a random string)
- Add a `requirements.txt` to the repo even if empty — this establishes the pattern for later
- Tag the repo with `v0.1.0` and publish it as a GitHub release
- Attach the Python script as a release asset

**Pass condition:** The script runs locally on your dev machine and prints a unique code each run.

---

## Phase 2 — PyInstaller bundle

**Goal:** Confirm the Python script and its environment can be frozen into a self-contained binary.

- Set up a virtual environment on your dev machine
- Install dependencies from `requirements.txt` into that environment
- Run PyInstaller on the script to produce a self-contained `.exe`
- Test the `.exe` on your dev machine — confirm it prints a unique code without needing Python installed
- If available, test the `.exe` on a second machine that does not have Python installed

**Pass condition:** The `.exe` runs and prints a unique code on a machine with no Python installation.

---

## Phase 3 — MCP wrapper

**Goal:** Wrap the binary in a minimal MCP server that Claude can call.

- Write an MCP server that exposes a single tool called `get_secret_code`
- The tool calls the bundled `.exe` and returns its output
- Test the MCP server manually from the command line to confirm it invokes the binary and returns the code correctly
- Add the MCP server to the GitHub repo and attach it as a release asset under `v0.1.0`

**Pass condition:** Running the MCP server locally and calling `get_secret_code` manually returns a unique code.

---

## Phase 4 — Installer `.exe`

**Goal:** Automate the setup steps so no engineer needs to touch the command line.

- Write an installer `.exe` that does the following in sequence:
  - Checks the GitHub releases API for the latest release tag
  - Downloads all release assets into a local installation folder
  - Writes the MCP server entry into Claude Desktop's config file
- Run the installer on your dev machine
- After it runs, open Claude Desktop's config file manually and confirm the entry was written correctly before opening Claude

**Pass condition:** Config file contains the correct MCP server entry pointing to the downloaded assets.

---

## Phase 5 — Claude end to end

**Goal:** Confirm Claude Desktop recognises the tool and can invoke it successfully.

- Open Claude Desktop
- Manually add the tool to a new chat or project via the + menu
- Ask Claude to call `get_secret_code` and report what it returns
- Confirm the returned value matches what the `.exe` produces when run directly

**Pass condition:** Claude returns a unique code that matches direct execution of the binary.

---

## Phase 6 — Update mechanism

**Goal:** Confirm the installer correctly detects and applies updates without any manual steps beyond running it.

- Modify the Python script to include a version prefix in the output (e.g. `v0.2.0 — <unique code>`)
- Rebuild the PyInstaller binary on your dev machine
- Tag and publish a new `v0.2.0` release on GitHub with the updated assets attached
- Run the installer `.exe` again on the engineer's machine
- Confirm it detects the version difference, downloads the new assets, and overwrites the old ones
- Ask Claude for the secret code again — confirm the output now includes the version prefix

**Pass condition:** Claude returns output reflecting the updated script with no manual changes to Claude Desktop or its config.

---

## What this proves end to end

| Layer | Validated by |
|---|---|
| GitHub as release distribution source | Phase 1 |
| PyInstaller self-contained bundling | Phase 2 |
| MCP wrapper invoking a binary | Phase 3 |
| Installer writing Claude Desktop config | Phase 4 |
| Claude Desktop recognising and calling the tool | Phase 5 |
| Automatic version detection and update | Phase 6 |

Once all six phases pass, the delivery pipeline is proven and the real BOM tooling (Vault reader, pcMRP reader, comparison logic) can be built on top of it with confidence.
