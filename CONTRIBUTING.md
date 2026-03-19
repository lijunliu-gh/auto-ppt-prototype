# Contributing

Thanks for contributing to Auto PPT Prototype.

## Before You Start

- Read `README.md` for project scope and usage modes.
- Read `PRODUCT.en.md` for positioning and boundaries.
- Read `INTEGRATION_GUIDE.en.md` if your change affects agent or service integration.

## Development Setup

1. Install Node.js 18 or newer.
2. Install dependencies:

```bash
npm install
```

3. Copy `.env.example` to `.env` only if you need model-backed runs.

## Local Validation

Run the smoke checks before opening a pull request:

```bash
npm run ci:smoke
```

This validates the main prototype paths:

- structured deck rendering
- source-aware generation
- revise flow
- JSON skill flow

## Contribution Scope

Good contribution areas:

- deck planning quality
- revise quality
- source ingestion
- schema validation
- docs and examples
- integration stability
- CI and test coverage

Please keep changes focused. Avoid mixing unrelated refactors into the same pull request.

## Pull Request Guidelines

- explain what changed and why
- mention affected user flows
- include sample commands used for verification
- update docs when behavior changes
- avoid committing generated files under `output/`

## Design Principles

- prefer trusted and user-provided sources over broad web search
- keep rendered slides visually clean
- preserve provenance in machine-readable form where possible
- treat this repository as an agent backend, not a full research agent

## Reporting Problems

- Use the issue templates when possible.
- For security-sensitive issues, do not open a public issue. Follow `SECURITY.md`.