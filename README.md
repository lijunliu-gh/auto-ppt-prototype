 # Auto PPT Prototype

 Open-source PowerPoint planning and rendering backend for AI agents working from trusted sources, uploaded materials, and explicit user requirements.

Status: experimental prototype intended for public GitHub distribution and early external integration.

 This repository is designed as an agent backend, not as a local-only PPT script.

 Use it when you want an upstream agent or workflow to:

 - collect user intent
 - gather trusted material
 - build a structured deck
 - render a final `.pptx`

 ## Documentation

 The documentation set is intentionally kept small and split by audience:

 - `README.md`: repository entry and quick navigation
 - `PRODUCT.*.md`: product framing and open-source positioning
 - `USER_GUIDE.*.md`: end-user usage guidance
 - `INTEGRATION_GUIDE.*.md`: agent and system integration guidance

 ### Language Navigation

 | Document | English | Simplified Chinese | Japanese |
 | --- | --- | --- | --- |
 | Product Overview | `PRODUCT.en.md` | `PRODUCT.zh-CN.md` | `PRODUCT.ja.md` |
 | User Guide | `USER_GUIDE.en.md` | `USER_GUIDE.zh-CN.md` | `USER_GUIDE.ja.md` |
 | Integration Guide | `INTEGRATION_GUIDE.en.md` | `INTEGRATION_GUIDE.zh-CN.md` | `INTEGRATION_GUIDE.ja.md` |

 ### Consolidation Note

 The previous `CAPABILITIES.*.md` files have been folded into the `PRODUCT.*.md` family to avoid maintaining two overlapping summaries.

 ## What It Does

 The current implementation supports:

 1. Deck creation from prompts
 2. Deck revision from natural-language instructions
 3. Trusted source ingestion from files and URLs
 4. JSON-schema validation before rendering
 5. `.pptx` rendering with `pptxgenjs`
 6. Agent-facing CLI, JSON skill, and HTTP interfaces

 ## Why It Exists

 Serious presentation generation is not just web search plus slide output.

 For realistic use cases, the system should prefer:

 1. user-uploaded material
 2. official product pages
 3. official documentation
 4. investor or financial material
 5. explicit user notes
 6. web search only as a fallback

 This repository handles the deck-planning and rendering layer inside that broader workflow.

 ## Quick Start

 Install dependencies:

 ```bash
 npm install
 ```

 Try the main flows:

 ```bash
 npm run generate
 npm run generate:source
 npm run revise:mock
 npm run skill:create
 npm run skill:server
 ```

 ## Main Interfaces

 ### CLI

 Create from prompt:

 ```bash
 node generate-from-prompt.js --prompt "Create an 8-slide product strategy deck"
 ```

 Create from prompt plus sources:

 ```bash
 node generate-from-prompt.js --mock --prompt "Create an 8-slide strategy deck" --source sample-source-brief.md
 ```

 Revise an existing deck:

 ```bash
 node revise-deck.js --deck output/generated-deck.json --prompt "Compress this deck to 6 slides"
 ```

 ### JSON Skill

 ```bash
 node agent-skill.js --request sample-agent-request.json --response output/agent-response.json
 ```

 ### HTTP

 Start the local service:

 ```bash
 npm run skill:server
 ```

 Then call:

 ```bash
 curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
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
 - source references are preserved in structured slide metadata
 - source references are exported into presenter notes

 The default output mode is `sourceDisplayMode = notes`.

 ## Supported Slide Layouts

 - `title`
 - `agenda`
 - `section`
 - `bullet`
 - `two-column`
 - `comparison`
 - `timeline`
 - `process`
 - `table`
 - `chart`
 - `quote`
 - `summary`
 - `closing`

 ## Repository Structure

 - `generate-ppt.js`: deck JSON to PPTX renderer
 - `deck-agent-core.js`: planning, revision, validation, and model logic
 - `source-loader.js`: source ingestion and extraction
 - `generate-from-prompt.js`: create CLI entrypoint
 - `revise-deck.js`: revise CLI entrypoint
 - `agent-skill.js`: JSON skill entrypoint
 - `skill-server.js`: HTTP wrapper
 - `deck-schema.json`: deck schema contract
 - `skill-manifest.json`: skill contract for integrators
 - `SKILL.md`: agent behavior guidance

 ## Recommended Usage Model

 The intended flow is:

 1. user provides goal, audience, and constraints
 2. user or upstream agent provides trusted material
 3. upstream agent organizes context
 4. this repository generates the initial deck
 5. the agent calls revise again after feedback

 ## Project Boundaries

 This repository is not yet:

 - a full research agent
 - a complete OCR or multimodal system
 - a production-grade brand template engine
 - a fine-grained provenance mapper at bullet or chart-point level

 For those capabilities, keep the responsibility in the upstream agent or workflow.

 ## Read Next

 - `PRODUCT.en.md` for product framing
 - `USER_GUIDE.en.md` for user-oriented instructions
 - `INTEGRATION_GUIDE.en.md` for agent and system integration details
- `GITHUB_SETUP.md` for GitHub repository metadata, topics, and release copy
- `PUBLISH_CHECKLIST.md` for the pre-publish git checklist

## License And Publishing

This repository is structured to be publishable as an open-source project and usable by external agent frameworks that can call Node.js scripts or local HTTP endpoints.

License: MIT. See `LICENSE`.
