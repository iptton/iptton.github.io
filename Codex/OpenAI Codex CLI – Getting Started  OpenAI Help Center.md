---
title: "OpenAI Codex CLI – Getting Started | OpenAI Help Center"
source: "https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started"
author:
published:
created: 2025-04-29
description:
tags:
  - "clippings"
---
## OpenAI Codex CLI – Getting Started

## Overview

OpenAI **Codex CLI** is an open‑source command‑line tool that brings the power of our latest reasoning models directly to your terminal. It acts as a lightweight coding agent that can **read, modify, and run code on your local machine** to help you build features faster, squash bugs, and understand unfamiliar code. Because the CLI runs locally, your source code never leaves your environment unless you choose to share it.

![](https://www.youtube.com/watch?v=FUq9qRwrDrI)

For more details about Codex, please check out the Github repo directly - [https://github.com/openai/codex](https://github.com/openai/codex).

## Key Functionality

- **Zero‑setup installation** – a single `npm install -g @openai/codex` (or `codex --upgrade`) gets you started.
- **Multimodal inputs** – pass text, screenshots, or diagrams and let the agent generate or edit code accordingly.
- **Rich approvals workflow** – choose how hands‑on you want to be with three distinct modes (see [Approval Modes](https://help.openai.com/en/articles/#h_4a7cc50285)).
- **Runs entirely in your terminal** – perfect for quick iteration without switching contexts.

## Approval Modes

| **Mode** | **What the Agent Can Do** | **When to Use** |
| --- | --- | --- |
| **Suggest** (default) | Read files. Proposes edits & shell commands, but *requires your approval* before making changes or executing commands. | Safe exploration, code reviews, learning a codebase. |
| **Auto Edit** | Read **and** write files automatically. Still asks before running shell commands. | Refactoring or repetitive edits where you want to keep an eye on side‑effects. |
| **Full Auto** | Read, write, and execute commands autonomously inside a sandboxed, network‑disabled environment scoped to the current directory. | Longer tasks like fixing a broken build or prototyping features while you grab a coffee. |

*Pro tip: Codex warns you before entering Auto Edit or Full Auto if the directory isn’t under version control.*

## Quick Start

1. **Install**: `npm install -g @openai/codex`
2. **Authenticate**: Export your OpenAI API key (`export OPENAI_API_KEY="<OAI_KEY>"`).
3. **Run in Suggest mode**: From your project root, type codex and ask for example: *“Explain this repo to me.”*
4. **Switch modes**: Add flags as needed:
	- `codex --auto-edit`
	- `codex --full-auto`
5. **Review outputs**: Codex prints proposed patches and shell commands inline. Approve, reject, or tweak as desired.

## FAQ

By default Codex targets **o4‑mini** for fast reasoning. You can specify any model available in the Responses API, e.g. `codex -m o3`. We’d also recommend [verifying](https://help.openai.com/en/articles/10910291-api-organization-verification) your developer account to start seeing chain of thought summaries in the API.

**No**. All file reads, writes, and command executions happen locally. Only your prompt, high‑level context, and optional diff summaries are sent to the model for generation.

Start Codex with the appropriate flag (`--suggest`, `--auto-edit`, `--full-auto`) or use the in‑session shortcut `/mode` to toggle.

Codex officially supports macOS and Linux. Windows support is experimental and may require WSL.

- Ensure you have a stable internet connection for API calls.
- Try `CTRL‑C` to cancel the current step and ask Codex to continue.
- If using *Full Auto* mode, confirm that the sandbox has permission to access required directories.

Run `codex --upgrade` at any time to fetch the latest release.

Open a discussion or file an issue in the [GitHub repo](https://github.com/openai/codex) or engage with other developers in the community via the [OpenAI Developer Community](https://community.openai.com/).

Did this answer your question?