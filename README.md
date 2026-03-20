# Auto PPT Prototype

[![Release](https://img.shields.io/github/v/release/lijunliu-gh/auto-ppt-prototype?label=release)](https://github.com/lijunliu-gh/auto-ppt-prototype/releases)
[![License](https://img.shields.io/github/license/lijunliu-gh/auto-ppt-prototype)](LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/lijunliu-gh/auto-ppt-prototype/smoke.yml?branch=main&label=CI)](https://github.com/lijunliu-gh/auto-ppt-prototype/actions/workflows/smoke.yml)

Open-source PowerPoint backend for AI agents working from trusted sources, uploaded material, and explicit presentation requirements.

Status: experimental prototype for early open-source integration.

Latest release: [v0.7.0](https://github.com/lijunliu-gh/auto-ppt-prototype/releases/tag/v0.7.0)

Quick links:

- [Documentation index](docs/README.md)
- [Release notes](https://github.com/lijunliu-gh/auto-ppt-prototype/releases/tag/v0.7.0)
- [Changelog](CHANGELOG.md)
- [Roadmap](ROADMAP.md)
- [Examples (EN)](docs/EXAMPLES.en.md)
- [Examples (ZH)](docs/EXAMPLES.zh-CN.md)
- [Examples (JA)](docs/EXAMPLES.ja.md)
- [Product overview](docs/PRODUCT.en.md)
- [User guide](docs/USER_GUIDE.en.md)
- [Integration guide](docs/INTEGRATION_GUIDE.en.md)
- [Repository map](docs/REPOSITORY_MAP.md)

## Start Here

- New here and want a PPT in a few minutes: start with the 3-minute Quick Start below.
- Want to understand the input format: inspect `examples/inputs/sample-deck-brief.md` and `examples/inputs/sample-deck-brief.json`.
- Want integration instead of manual CLI usage: start with `examples/inputs/sample-agent-request.json` or `examples/inputs/sample-http-request.json`.

Architecture summary:

- Python plans and revises decks
- JavaScript renders final `.pptx` files
- deck JSON is the stable contract between both layers

## Contents

- [3-Minute Quick Start](#3-minute-quick-start)
- [Core Positioning](#core-positioning)
- [What It Does](#what-it-does)
- [Quick Start](#quick-start)
- [MCP Server](#mcp-server)
- [Repository Map](#repository-map)
- [Testing](#testing)
- [End-To-End Flow](#end-to-end-flow)
- [Main Interfaces](#main-interfaces)
- [Source Handling](#source-handling)
- [Recommended Usage Model](#recommended-usage-model)
- [Project Boundaries](#project-boundaries)
- [Documentation](#documentation)
- [License](#license)

## Core Positioning

This repository is now intentionally split into two layers:

- Python smart layer: planning, revision, source ingestion, model calls, and agent-facing orchestration
- JavaScript render layer: validated deck JSON to `.pptx` output with `pptxgenjs`

The recommended mental model is:

`requirements + trusted material -> Python planning -> deck JSON -> JavaScript rendering -> PPTX`

This is an agent backend, not a standalone research agent and not just a local slide script.

## Who This Is For

- teams building AI agents that need PPT output
- developers who want a local PPT generation backend
- workflows that start from trusted files, URLs, or structured briefs
- users who want first-draft generation plus revision loops

## Who This Is Not For

- users looking for a hosted end-user SaaS product
- users expecting a fully autonomous research agent
- teams that need production-grade brand template control today
- users who only want a lightweight markdown-to-slides converter

## What It Does

The current implementation supports:

1. Prompt-to-deck planning
2. Natural-language deck revision
3. Trusted source ingestion from local files and URLs
4. JSON-schema validation before rendering
5. Agent-callable CLI, JSON skill, and local HTTP service entrypoints
6. PPTX rendering through the Node renderer
7. Pluggable LLM provider layer (OpenAI, OpenRouter, Claude, Gemini, and OpenAI-compatible endpoints)
8. Security hardening: path traversal protection, SSRF blocking, file size limits, subprocess timeout
9. Structured logging across the Python backend
10. Schema versioning for forward-compatible deck migration
11. MCP Server for native integration with Claude Desktop, Cursor, Windsurf, and other MCP-compatible environments
12. API versioning (`apiVersion: "1.0"`) in all requests and responses

## 3-Minute Quick Start

If this is your first time using the project, do only these steps.

### 1. Install dependencies

```bash
npm install
python -m pip install -r requirements.txt
```

### 2. Initialize local config

```bash
./auto-ppt init
```

This writes a local `.env` file with your provider key, default model, and default output directory.

If you only want to prove the pipeline works before configuring a real model, you can skip `init` and use `--mock` in the next step.

### 3. Generate your first deck

Mock mode, fastest proof that the repo works:

```bash
./auto-ppt generate --mock --prompt "Create an 8-slide AI workspace strategy deck for executives" --source examples/inputs/sample-source-brief.md
```

Real model, after `init`:

```bash
./auto-ppt generate --prompt "Create an 8-slide AI workspace strategy deck for executives" --source examples/inputs/sample-source-brief.md
```

### 4. Revise the generated deck

```bash
./auto-ppt revise --deck output/py-generated-deck.json --prompt "Compress this deck to 6 slides and make it more conclusion-driven"
```

What you should expect after a successful run:

- `output/py-generated-deck.json`
- `output/py-generated-deck.pptx`
- `output/py-revised-deck.json`
- `output/py-revised-deck.pptx`

After this first run, keep reading if you need MCP, HTTP service, templates, Docker, or deeper integration.

## Why The Split Exists

The Python layer is the right place for future intelligence work:

- source understanding
- document parsing
- model orchestration
- retrieval and multimodal expansion
- more advanced revision logic

The JavaScript layer already has a working renderer and remains the stable output engine.

That gives the project a clear boundary:

- Python owns intelligence
- Node owns rendering

## Quick Start

This section lists the main entrypoints after your first successful run.

Install dependencies:

```bash
npm install
python -m pip install -r requirements.txt
```

### 1. Official CLI first run

Initialize local config once:

```bash
./auto-ppt init
```

This writes a local `.env` file with your provider key, default model, and default output directory.

Then generate your first deck:

```bash
./auto-ppt generate --mock --prompt "Create an 8-slide AI workspace strategy deck for executives" --source examples/inputs/sample-source-brief.md
```

If you want predictable filenames for repeated runs, add `--output-name`:

```bash
./auto-ppt generate --prompt "Create an 8-slide AI workspace strategy deck for executives" --source examples/inputs/sample-source-brief.md --output-name workspace-strategy-v1
```

### 2. Revise the generated deck

```bash
./auto-ppt revise --deck output/py-generated-deck.json --prompt "Compress this deck to 6 slides and make it more conclusion-driven"
```

`revise` now follows the same output rules as `generate`:

- `--output-dir` changes the directory for JSON and PPTX output
- `--output-name` changes the base filename for JSON and PPTX output
- if `AUTO_PPT_OUTPUT_DIR` is configured, `revise` also uses it to locate the default input deck

The legacy scripts (`py-generate-from-prompt.py`, `py-revise-deck.py`) remain available, but `auto-ppt` is now the official user-facing CLI entrypoint.

### 3. File-based agent integration

```bash
python py-agent-skill.py --request examples/inputs/sample-agent-request.json --response output/py-agent-response.json
```

### 4. Local HTTP service

```bash
python py-skill-server.py
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @examples/inputs/sample-http-request.json
```

### 5. MCP Server (Claude Desktop / Cursor / Windsurf)

```bash
python mcp_server.py
```

Or use the MCP dev inspector:

```bash
mcp dev mcp_server.py
```

See [MCP Server](#mcp-server) below for client configuration.

### 6. npm shortcuts

```bash
npm run generate
npm run generate:source
npm run revise:mock
npm run skill:create
npm run skill:server
```

Useful starter files:

- `examples/inputs/sample-source-brief.md`: shortest source-grounded example
- `examples/inputs/sample-deck-brief.md`: natural-language deck brief example
- `examples/inputs/sample-deck-brief.json`: structured deck brief example
- `examples/inputs/sample-agent-request.json`: JSON skill request example
- `examples/inputs/sample-http-request.json`: HTTP request example
- `quality_samples/`: fixed Phase 7 quality-evaluation corpus for regression work

If you want copy-paste usage flows, start with `docs/EXAMPLES.en.md`, `docs/EXAMPLES.zh-CN.md`, or `docs/EXAMPLES.ja.md`.

## MCP Server

The MCP server exposes `create_deck` and `revise_deck` as native MCP tools, enabling direct integration with Claude Desktop, Cursor, Windsurf, and other MCP-compatible AI environments.

### Claude Desktop configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) or `%APPDATA%\Claude\claude_desktop_config.json` (Windows):

```json
{
  "mcpServers": {
    "auto-ppt": {
      "command": "python",
      "args": ["/absolute/path/to/auto-ppt-prototype/mcp_server.py"]
    }
  }
}
```

### Cursor / Windsurf configuration

Add to `.cursor/mcp.json` or `.windsurf/mcp.json` in your project root:

```json
{
  "mcpServers": {
    "auto-ppt": {
      "command": "python",
      "args": ["/absolute/path/to/auto-ppt-prototype/mcp_server.py"]
    }
  }
}
```

### Available tools

| Tool | Description |
|------|-------------|
| `create_deck` | Create a new PowerPoint deck from a natural-language prompt |
| `revise_deck` | Revise an existing deck based on a natural-language instruction |

Both tools accept `sources` (file paths or URLs), `mock` mode for offline testing, and optional `output_dir`.

## Repository Map

For the full file-by-file map, see [docs/REPOSITORY_MAP.md](docs/REPOSITORY_MAP.md).

High-level split:

- `python_backend/` owns planning, revision, source understanding, and orchestration
- `docs/` holds multilingual user and integration documentation
- `examples/inputs/` holds quickstart payloads and source briefs
- `quality_samples/` holds the fixed Phase 7 quality-regression corpus
- `tests/` holds pytest coverage for backend and integrations

## Testing

Run the unit test suite (282 tests, 85% coverage):

```bash
python -m pytest tests/ -v
```

Run smoke tests:

```bash
npm run ci:smoke
```

Or run individual smoke steps:

```bash
npm run smoke:generate   # JS renderer smoke
npm run smoke:source     # Source-grounded generation
npm run smoke:revise     # Revision flow
npm run smoke:skill      # Agent skill workflow
```

CI runs pytest across Python 3.10, 3.11, and 3.12, plus Node.js 18, 20, and 22 smoke tests.

## Docker

Single-command launch via Docker Compose:

```bash
# Set your LLM provider key
export OPENAI_API_KEY="sk-..."

# Build and start the HTTP skill server
docker compose up --build

# Or run the MCP server (stdio) directly
docker run --rm -it -e OPENAI_API_KEY auto-ppt-prototype python mcp_server.py

# Or run with remote MCP transport (Streamable HTTP)
docker run --rm -p 8080:8080 -e OPENAI_API_KEY auto-ppt-prototype \
  python mcp_server.py --transport streamable-http --host 0.0.0.0 --port 8080
```

## End-To-End Flow

```mermaid
flowchart TD
        A[Deck brief or prompt] --> C[Python entrypoint]
        B[Trusted sources] --> D[Source loader]
        M[MCP Client] -->|create_deck / revise_deck| K[MCP Server]
        K --> C
        C --> D
        D --> E[Smart layer]
        E --> F[Validated deck JSON]
        F --> G{Template?}
        G -->|No| H[JS bridge → pptxgenjs]
        G -->|Yes| P[python-pptx renderer]
        H --> I[PPTX output]
        P --> I
        E -. revise loop .-> C
        F --> J[Notes with source metadata]
        IMG[Image handler] -.->|resolve images| P
        IMG -.->|resolve images| H

        subgraph Inputs
            A
            B
            M
        end

        subgraph Python
            K
            C
            D
            E
            IMG
        end

        subgraph Contract
            F
        end

        subgraph Render
            G
            H
            P
            I
            J
        end
```

The operational flow is:

- an upstream agent, MCP client, or caller provides the deck goal and any presentation constraints
- MCP-compatible clients (Claude Desktop, Cursor, Windsurf) connect through the MCP Server, which routes to the same Python entrypoint
- trusted source material is loaded and normalized before planning
- the Python layer produces or revises validated deck JSON
- if a brand template is provided, the python-pptx renderer produces the PPTX; otherwise the JS bridge invokes pptxgenjs
- the image handler resolves and validates visual assets before rendering
- revision requests loop back into the same Python planning surface

## Main Interfaces

### Python-first CLI

Create a deck:

```bash
python py-generate-from-prompt.py --mock --prompt "Create an 8-slide product strategy deck"
```

Revise a deck:

```bash
python py-revise-deck.py --mock --deck output/py-generated-deck.json --prompt "Compress this deck to 6 slides"
```

### Compatibility Node CLI

These files still exist for backward compatibility, but they now forward into the Python smart layer:

- `compat/generate-from-prompt.js`
- `compat/revise-deck.js`
- `compat/agent-skill.js`
- `compat/skill-server.js`

### JSON Skill

```bash
python py-agent-skill.py --request examples/inputs/sample-agent-request.json --response output/py-agent-response.json
```

### HTTP

Start the default service:

```bash
npm run skill:server
```

Call the endpoint:

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @examples/inputs/sample-http-request.json
```

## Source Handling

Supported source types:

- local text-like files: `.txt`, `.md`, `.csv`, `.json`, `.yaml`, `.xml`
- local HTML
- local PDF
- local DOCX
- image references
- HTTP and HTTPS URLs

Current default behavior:

- slide body stays clean
- sources are preserved in structured slide metadata
- sources are exported into presenter notes

The default output mode is `sourceDisplayMode = notes`.

## Recommended Usage Model

The intended flow is:

1. an upstream agent collects the user goal and constraints
2. the upstream agent gathers trusted material
3. the Python smart layer plans or revises the deck JSON
4. the Node renderer produces the final PPTX
5. the upstream agent calls revise again when feedback arrives

## Project Boundaries

This repository is not yet:

- a full autonomous research agent
- a complete OCR or multimodal system
- a production-grade brand template engine
- a fine-grained bullet-level provenance mapper

Those responsibilities should remain with the upstream agent or surrounding workflow.

## Documentation

- `docs/README.md`: documentation index and reading order
- `EXAMPLES.*.md`: copy-paste usage flows for first-time users
- `PRODUCT.*.md`: product framing and open-source positioning
- `USER_GUIDE.*.md`: end-user usage guidance
- `INTEGRATION_GUIDE.*.md`: agent and system integration guidance
- `CHANGELOG.md`: version history and release tracking
- `ROADMAP.md`: planned evolution and feature priorities

## Read Next

- `docs/README.md` for the organized documentation index
- `docs/PRODUCT.en.md` for product framing
- `docs/EXAMPLES.en.md` for first-run examples
- `docs/USER_GUIDE.en.md` for user-oriented instructions
- `docs/INTEGRATION_GUIDE.en.md` for integration details
- `RELEASE_CHECKLIST.md` for the release checklist

## License

MIT. See `LICENSE`.
