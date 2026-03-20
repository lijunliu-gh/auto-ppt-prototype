# Quality Samples

This directory is the Phase 7 golden prompt set for output-quality work.

These files are not the same as the root-level `sample-*` demo inputs.

- Root-level `sample-*` files are quickstart and integration examples.
- `quality_samples/` is a fixed evaluation corpus for regression checks.

## Goals

- keep a stable set of representative deck-generation scenarios
- cover both first-pass generation and revise flows
- make future quality work comparable across changes
- document what a good result should roughly look like

## Layout

- `manifest.json`: top-level index of all quality cases
- `cases/*.json`: per-case definitions with prompt, sources, and acceptance notes
- `sources/*.md`: reusable source material for source-grounded cases

## Current Coverage

The first version includes 10 cases:

- 7 generate cases
- 3 revise cases
- categories: strategy, product review, board update, operations, market synthesis, policy briefing, education

## How To Use

Today, this directory is a human-readable and test-validated corpus.

It is intended to support the next Phase 7 steps:

1. apply a quality scorecard against the same fixed inputs
2. compare outputs before and after prompt or planner changes
3. add automated regression checks over time

## Case Conventions

Each case file records:

- `caseId`: stable identifier
- `mode`: `generate` or `revise`
- `category`: scenario family
- `prompt`: initial request or revise instruction
- `sources`: supporting source files under `quality_samples/sources/`
- `inputCaseId`: for revise cases, the generate case that should be produced first
- `acceptanceNotes`: what a reasonable output should accomplish
- `regressionFocus`: what future comparisons should pay attention to

## Notes

- These cases do not require a single exact deck output.
- They are intended for relative quality comparison, not snapshot testing of wording.
- New cases should expand scenario coverage, not duplicate an existing category unless they add a new failure mode.
