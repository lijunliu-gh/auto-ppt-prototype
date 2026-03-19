# v0.3.0 - Python planning layer with JavaScript PPTX renderer

This release moves Auto PPT Prototype to a Python-first public architecture while keeping the JavaScript renderer as the stable PPTX output engine.

### What changed

- new Python smart layer for planning, revision, source loading, and agent orchestration
- JavaScript renderer retained as the final `.pptx` output engine
- Node create, revise, skill, and server entrypoints kept as compatibility wrappers
- Python-first CLI, JSON skill, and HTTP service flows
- refreshed English, Simplified Chinese, and Japanese documentation for the new architecture
- repository homepage and release materials reorganized for clearer GitHub presentation

### Architecture summary

The repository now exposes a clearer execution model:

- Python owns planning, revision, source ingestion, and agent-facing orchestration
- deck JSON remains the stable contract between planning and rendering
- JavaScript focuses on deterministic PPTX generation through `pptxgenjs`

### Compatibility

- existing Node entrypoints still work for older integrations
- new integrations should treat Python as the primary public entrypoint surface
- deck JSON remains the stable contract between planning and rendering

### Validation

- Python create, revise, and skill flows were validated locally
- compatibility wrappers were validated after Windows argument forwarding fixes
- the smoke workflow now validates the Python-first revise flow correctly in GitHub Actions
- local health checks confirmed the Python skill server on port `3010`

### Current boundaries

- this is still an experimental prototype
- the repository is an agent backend, not a full research agent
- OCR, stronger provenance mapping, and production-grade template control are still future work