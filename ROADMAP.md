# Roadmap

Current version: **v0.7.0**

This roadmap reflects the project's current capabilities, known gaps, and planned evolution from experimental prototype to a productized AI-agent PowerPoint backend.

The first five roadmap phases are complete. All 14 original GitHub issues are closed. Phase 5 (v0.7.0) added deployment packaging and chart determinism improvements. The next roadmap focus is first-run product experience: make the project immediately usable for someone who only wants to configure an API key and generate a deck.

---

## Current Baseline (v0.3.1)

| Capability | Status |
|------------|--------|
| Python planning + JS rendering + JSON contract | ✅ Stable |
| 13 slide layouts (title, bullet, timeline, chart, table, etc.) | ✅ |
| Chart / Table schema + rendering | ✅ Schema and renderer exist; LLM planning rarely generates valid chart data |
| Source ingestion (PDF, DOCX, HTML, TXT, JSON, URL) | ✅ |
| Security hardening (path traversal, SSRF, file size, subprocess timeout) | ✅ Added in v0.3.1 |
| Pluggable LLM provider abstraction | ✅ Added in v0.3.1 |
| Structured logging | ✅ Added in v0.3.1 |
| Schema versioning | ✅ Added in v0.3.1 |
| Unit tests (39 pytest cases) | ✅ Added in v0.3.1 (now 282 tests, 85% coverage as of v0.7.0) |
| CLI / JSON Skill / HTTP Server | ✅ |

---

## Phase 1 — MCP Server + Ecosystem Integration → v0.4.0 ✅

**Status**: Complete — released in v0.4.0

**Goal**: Enable native invocation from Claude Desktop, Cursor, Windsurf, and other MCP-compatible AI environments.

| Task | Description | Complexity |
|------|-------------|------------|
| Implement MCP Server | Expose `create_deck` and `revise_deck` as MCP tools via the `mcp` Python SDK | Medium |
| MCP tool schema | Map existing `skill-manifest.json` actions to MCP tool definitions | Low |
| Security boundary | MCP runs locally but must enforce file access scope (reuse v0.3.1 path traversal protection) | Low (already done) |
| Integration test | End-to-end script: MCP call → deck JSON → PPTX output | Medium |
| Documentation | Add MCP config examples for Claude Desktop and Cursor | Low |

**Why first**: Security prerequisites are met (v0.3.1). Implementation reuses existing HTTP server logic. Highest leverage for user acquisition — one MCP server makes the tool callable from every MCP-compatible environment with zero friction.

**Deliverables**: `mcp_server.py`, Cursor / Claude Desktop config examples, integration tests.

---

## Phase 2 — Chart Data Reliability + Multi-Model Validation → v0.4.1 ✅

**Status**: Complete — released in v0.4.1

**Goal**: Make LLM-generated chart and table data actually usable (not empty placeholders).

| Task | Description | Complexity |
|------|-------------|------------|
| Strengthen chart prompts | Add chart data generation constraints and few-shot examples to system prompt | Low |
| Source → chart mapping | When sources contain numerical data (CSV, JSON, tables), auto-extract and inject into chart context | Medium |
| Multi-model testing | Run planning through Claude, GPT-4.1, Gemini; compare schema pass rate and chart fill rate | Medium |
| Chart fallback | When LLM-generated chart data is invalid, fall back to bullet layout + assumption declaration | Low |

**Why here**: The schema and renderer already support charts — the real bottleneck is LLM planning quality. The v0.3.1 LLM provider abstraction makes multi-model testing straightforward.

---

## Phase 3 — Brand Template Engine → v0.5.0 ✅

**Status**: Complete — released in v0.5.0

**Goal**: Accept a user-provided `.pptx` master template and produce brand-matched output.

| Task | Description | Complexity |
|------|-------------|------------|
| Template parsing | Read `.pptx` slide layouts + placeholders via `python-pptx` | High |
| Layout mapping | Build a config that maps schema layouts → master slide layouts | Medium |
| Dual render path | No template → existing JS renderer; with template → Python `python-pptx` placeholder injection | High |
| Schema extension | Add `template` field to deck JSON (template path + layout mapping overrides) | Low |
| Sample templates | Ship 2–3 ready-to-use brand templates (tech, business, education) | Medium |

**Why here, not earlier**: This is the biggest usability leap, but also the highest implementation cost. It may require introducing `python-pptx` as a second render path alongside `pptxgenjs`. Best tackled after MCP and chart reliability have established a user base.

**Risk**: May require re-evaluating whether to keep the JS render layer or migrate entirely to `python-pptx`.

---

## Phase 4 — Image Asset Pipeline → v0.5.1 ✅

**Status**: Complete — released in v0.5.1

**Goal**: Support image insertion and lay the groundwork for multi-agent image collaboration.

| Task | Description | Complexity |
|------|-------------|------------|
| Local image insertion | `visuals` field accepts local file paths / URLs → renderer actually inserts images | Medium |
| Image placeholder protocol | `visuals` supports `{"type": "placeholder", "prompt": "...", "position": "right"}` | Low |
| Two-pass rendering | First pass: render with blank placeholders + annotations → external agent fills images → second pass: final render | Medium |
| Size / position constraints | Renderer auto-calculates image region size to prevent overflow | Medium |

**Why last**: Text content is the core value of any presentation. Image support is important but additive. Start with local image insertion (practical), then add the placeholder protocol (interface for multi-agent ecosystems).

---

## Phase 5 — Deployment Packaging + Chart Determinism + Remote MCP → v0.7.0 ✅

**Status**: Complete — released in v0.7.0

**Goal**: Lower deployment friction, improve chart reliability, and enable remote MCP access.

| Task | Description | Complexity |
|------|-------------|------------|
| Docker packaging | `Dockerfile` (Python 3.12 + Node.js 20) + `docker-compose.yml` for one-command launch | Medium |
| Chart auto-repair | `repair_chart_data()` — fix invalid types, coerce string-formatted numbers, trim excess data; degrade to bullet on irreparable data | Medium |
| Stricter chart schema | `enum` for chart types, `minItems` on categories/series, `oneOf` for empty vs valid charts | Low |
| Remote MCP transport | `--transport streamable-http --host --port` CLI args for hosted deployments | Low |
| Documentation sync | Docker, remote MCP, and smoke command fixes across all multilingual docs | Low |

**Why here**: Evaluation report identified deployment friction, chart determinism, remote MCP, and documentation drift as the four highest-priority gaps.

---

## Phase 6 — CLI-First Immediate Experience → v0.8.0

**Status**: Planned

**Goal**: Give first-time users a single official entrypoint that can generate a PPT after minimal setup.

| Task | Description | Complexity |
|------|-------------|------------|
| Official CLI entrypoint | Introduce a single `auto-ppt` command instead of exposing multiple top-level scripts as the primary user path | Medium |
| `auto-ppt init` | Interactive setup for provider selection, API key wiring, default model, and output directory | Medium |
| `auto-ppt generate` / `revise` | Unified user-facing commands for create / revise flows with predictable flags and output paths | Medium |
| User-grade error messages | Replace raw traceback-first UX with actionable setup and retry guidance | Low |
| 3-minute quickstart | Rewrite top-level docs around the shortest successful path for first-time use | Low |

**Why next**: The biggest remaining gap is no longer backend capability; it is first-run success rate. The project already has multiple working execution paths, but they are too fragmented for someone encountering the tool for the first time.

---

## Phase 7 — Real-World Output Quality Control → v0.8.1

**Status**: Planned

**Goal**: Make generated decks consistently closer to what a real user expects, not just syntactically valid.

| Task | Description | Complexity |
|------|-------------|------------|
| Golden prompt set | Build 10-20 representative user scenarios (strategy, product, news analysis, source-grounded summary, executive review) | Low |
| Quality scorecard | Define pass/fail criteria for structure, audience fit, source grounding, chart usage, and revision usefulness | Medium |
| Planning guardrails | Add explicit controls for audience, tone, page budget, and slide structure | Medium |
| Revision loop hardening | Improve revise prompts and heuristics so users can reliably turn a first draft into a usable deck | Medium |

**Why after Phase 6**: A simpler entrypoint only matters if the resulting deck quality is stable enough for repeated use. This phase converts "it works" into "it usually gives me something close to what I wanted".

---

## Phase 8 — Packaging and Distribution → v0.9.0

**Status**: Planned

**Goal**: Reduce installation friction so users can run the tool without understanding the Python + Node implementation split.

| Task | Description | Complexity |
|------|-------------|------------|
| Installable CLI | Publish a clean install path such as `pipx` or `uvx` for the official CLI | Medium |
| Bootstrap assets | Provide `.env.example`, provider presets, and install-time validation | Low |
| Docker-first quickstart | Keep Docker as the zero-dependency fallback path for local or team deployment | Low |
| Output UX polish | Improve default output location, naming, and success messages for generated artifacts | Low |

**Why here**: Once the CLI path and deck quality are coherent, packaging work has a stable product surface to wrap.

---

## Phase 9 — Minimal End-User UI → v1.0.0

**Status**: Future

**Goal**: Expose the core generate/revise loop to non-command-line users through the thinnest possible interface.

| Task | Description | Complexity |
|------|-------------|------------|
| Minimal web UI | Prompt input, source upload, optional audience/page controls, and PPTX download | Medium |
| Job status feedback | Show progress and final artifact locations clearly | Medium |
| Template/source affordances | Basic upload flows for templates and supporting source documents | Medium |
| Reuse CLI core | UI must call the same stable core interfaces introduced in Phase 6 rather than fork product logic | Low |

**Why later**: UI should package a stable workflow, not hide an unstable one. The CLI and quality-control phases need to define the correct product semantics first.

---

## Ongoing (Across All Phases)

| Task | Description |
|------|-------------|
| Remove legacy JS code | ~~After Phase 1, delete `deck-agent-core.js` and `source-loader.js` entirely~~ ✅ Done in v0.4.1 |
| Expand test coverage | ✅ Achieved 85% coverage with 282 tests in v0.7.0 (Issue #12) |
| API versioning | ✅ `apiVersion: "1.0"` in all requests and responses (v0.6.0, Issue #13) |
| CI hardening | ✅ pytest on Python 3.10/3.11/3.12 + Node.js 18/20/22 smoke matrix (v0.6.0, Issue #14) |
| Documentation sync | Update EN / ZH / JA docs with each release |

---

## Timeline Summary

```text
v0.4.0   MCP Server               ← Highest leverage, do first     ✅
v0.4.1   Chart reliability         ← Prove core quality             ✅
v0.5.0   Brand template engine     ← Usability breakthrough         ✅
v0.5.1   Image pipeline            ← Ecosystem expansion            ✅
v0.6.0   API versioning + CI + coverage ← All issues resolved       ✅
v0.7.0   Docker + chart repair + remote MCP ← Deployment-ready      ✅
v0.8.0   CLI-first onboarding      ← First-run user success         Planned
v0.8.1   Quality control           ← Real-world output reliability  Planned
v0.9.0   Packaging / distribution  ← Easier install and setup       Planned
v1.0.0   Minimal UI                ← Non-CLI usability              Future
```

---

## Contributing

If you are interested in contributing to any of these areas, see [CONTRIBUTING.md](CONTRIBUTING.md) and open an issue to discuss your approach before starting work.
