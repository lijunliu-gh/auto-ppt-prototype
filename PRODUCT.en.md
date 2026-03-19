# Product Capability Summary

## Current Product

Auto PPT Prototype is an open-source PowerPoint generation backend for AI agents.

It provides:

- deck planning from prompts
- deck revision from natural-language instructions
- JSON schema validation
- `.pptx` rendering
- agent-callable JSON request and response flow
- local HTTP skill endpoint

## What It Is

It is a planning-and-rendering engine.

It is meant to sit behind an AI agent that can:

- collect requirements
- ask clarifying questions
- retrieve trusted material
- read uploaded documents
- inspect screenshots or images
- decide what content belongs on each slide

## What It Is Not

It is not a complete research agent by itself.

It should not be described as a simple web-search-to-slide generator.

For serious use cases, the system should rely on:

1. official sources
2. user-uploaded source material
3. explicit user instructions
4. general web search only as a fallback

## Current Interfaces

- CLI generation
- CLI revision
- JSON request/response skill wrapper
- HTTP service wrapper

## Production Gaps

- source ingestion for PDF, DOCX, HTML, CSV, and spreadsheets
- image and screenshot understanding
- provenance tracking
- stronger theme/template support
- better layout quality and typography control
- automated testing
- hosted deployment hardening

## Recommended Open-Source Framing

Recommended GitHub description:

> Open-source PowerPoint planning and rendering backend for AI agents working from trusted sources, uploaded materials, and explicit user requirements.
