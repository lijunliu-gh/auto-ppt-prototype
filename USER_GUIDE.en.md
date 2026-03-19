# User Guide

This document is written for users rather than developers.

If you want to know what the project can do today, what scenarios it fits, and how to operate it step by step, start here.

## What This Is

This is a PowerPoint generation backend prototype that can be called by an AI agent.

It is not just a template script, and it is not a complete research agent.

A practical way to think about it is:

- the upstream AI agent understands the request, gathers materials, runs research, and organizes context
- this project turns that input into deck JSON and then renders a PowerPoint file

In short:

`requirements + source material -> deck JSON -> PPTX`

## Good Use Cases

The current version is a good fit for:

- product strategy presentations
- executive review decks
- sales proposal decks
- project retrospectives
- first-draft training decks
- presentations grounded in official sites, PDFs, DOCX files, or Markdown briefs
- workflows where you generate a first draft and then revise it multiple times

## What It Can Do Today

### 1. Generate PPT directly from existing JSON

Use this when you already have structured deck data.

Command:

```bash
npm run generate
```

Input file:

- `sample-input.json`

Output file:

- `output/sample-deck.pptx`

### 2. Generate PPT from a natural-language prompt

Use this when you only have a rough request.

Command:

```bash
npm run generate:mock
```

If a model is configured, you can also run:

```bash
npm run generate:prompt
```

Direct example:

```bash
node generate-from-prompt.js --prompt "Create an 8-slide AI product strategy deck for executives in a professional tone"
```

### 3. Generate PPT with source material

This is the recommended path for most real use cases.

Use it when you can provide material in addition to the request, such as:

- product briefs
- official URLs
- PDFs
- DOCX files
- Markdown notes

Command:

```bash
npm run generate:source
```

This script reads:

- `sample-source-brief.md`

You can also pass your own sources:

```bash
node generate-from-prompt.js --mock --prompt "Create an 8-slide strategy deck" --source your-brief.md --source https://example.com/product
```

### 4. Revise an existing deck

Use this after you already generated a first draft and want to improve it.

Typical revision requests include:

- reduce the slide count
- make it more conclusion-driven
- emphasize the execution plan
- reorganize the structure
- make it more suitable for executives

Command:

```bash
npm run revise:mock
```

Direct example:

```bash
node revise-deck.js --deck output/generated-deck.json --prompt "Compress this deck, make it more conclusion-driven, and emphasize the execution plan"
```

### 5. Use it as a skill from another agent

Use this when you want to connect the project to another agent workflow.

Commands:

```bash
npm run skill:create
npm run skill:revise
```

Related files:

- `agent-skill.js`
- `sample-agent-request.json`
- `sample-agent-revise-request.json`
- `skill-manifest.json`

### 6. Use it as an HTTP service

Use this when your system prefers API-style local integration.

Start the service:

```bash
npm run skill:server
```

Health check:

```bash
curl http://localhost:3010/health
```

Call the endpoint:

```bash
curl -X POST http://localhost:3010/skill -H "Content-Type: application/json" --data @sample-http-request.json
```

## How Source Material Works

This is one of the most important parts of the current product.

Supported source types include:

- local text files: `txt`, `md`, `csv`, `json`, `yaml`, `xml`
- local HTML
- local PDF
- local DOCX
- image file references
- HTTP / HTTPS URLs

### Current Source Display Strategy

By default:

- slide body content does not show sources
- presenter notes do show sources
- per-slide sources are also preserved in structured metadata

That means:

- audience-facing slides stay clean
- the presenter can still see the source basis in notes
- the system can continue to use those sources during revise or audit flows

## Recommended Workflow

If you want to use this project for a relatively rigorous presentation, do not rely on a prompt alone.

The better workflow is:

1. Define the presentation goal.
2. Provide source material.
3. Generate a first draft.
4. Run 1 to 3 revision rounds.

Example:

1. You provide the goal.
   Example: an 8-slide product strategy deck for executives.
2. You provide materials.
   Example: a product brief, official URLs, a market analysis PDF, and an internal project memo.
3. Generate the first draft.
   Use `generate-from-prompt.js`.
4. Revise it.
   Compress it to 6 slides, make it more conclusion-driven, strengthen the execution plan, or retarget it for investors.

## Three Commands To Try First

If you only want to try the project quickly, use these three commands in order.

### Step 1: Try source-aware generation

```bash
npm run generate:source
```

### Step 2: Try skill mode

```bash
npm run skill:create
```

### Step 3: Try revise mode

```bash
npm run revise:mock
```

## What The Main Files Do

### Most relevant files for users

- `README.md`
  - main English overview
- `PRODUCT.en.md`
  - English product summary and project framing
- `USER_GUIDE.zh-CN.md`
  - Simplified Chinese user guide
- `sample-input.json`
  - sample deck input
- `sample-source-brief.md`
  - sample source material
- `sample-agent-request.json`
  - sample create request for skill mode
- `sample-agent-revise-request.json`
  - sample revise request for skill mode
- `sample-http-request.json`
  - sample HTTP request

### Core files for technical integration

- `generate-ppt.js`
  - render deck JSON into PPT
- `generate-from-prompt.js`
  - generate deck and PPT from a prompt
- `revise-deck.js`
  - revise an existing deck
- `deck-agent-core.js`
  - planning, revise, and schema-validation core
- `source-loader.js`
  - source loading and extraction
- `agent-skill.js`
  - JSON skill entrypoint
- `skill-server.js`
  - HTTP skill entrypoint
- `deck-schema.json`
  - deck JSON contract
- `skill-manifest.json`
  - skill integration contract

## Where It Is Still Weak

The project already supports a complete prototype workflow, but it is not yet a production-grade product.

Current weak points include:

- it is not a complete research agent
- OCR and multimodal understanding are not fully implemented
- slide-level source binding is still coarse
- brand templates and visual control are still basic
- complex scenarios still depend heavily on the quality of the upstream model and agent

## How To Understand This Project

The best way to understand it is as a:

- PPT skill backend for AI agents
- deck planning engine that can read source material
- PowerPoint prototype system that outputs `.pptx`

Its core value is not that it is a local command-line toy.

Its core value is:

**it already has the structure needed to be called by a larger AI agent workflow.**

## One-Line Summary

Today this folder can already complete:

- `prompt -> deck -> pptx`
- `prompt + sources -> deck -> pptx`
- `existing deck + revise prompt -> revised deck -> pptx`
- `agent request -> skill response`
- `HTTP request -> generated PPT artifacts`