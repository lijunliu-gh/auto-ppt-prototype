# Security Policy

## Supported Scope

This repository is an experimental open-source prototype. Security fixes may be accepted on a best-effort basis.

## Reporting A Vulnerability

Please do not file public GitHub issues for suspected vulnerabilities.

Instead, report them privately to the maintainers through your preferred private channel before public disclosure.

When reporting, include:

- affected file or feature
- reproduction steps
- potential impact
- suggested mitigation if known

## What Counts As Security-Relevant

Examples include:

- unsafe handling of uploaded or local files
- SSRF-like issues through URL source loading
- path traversal through request inputs
- accidental credential exposure
- unsafe HTTP service behavior

## Prototype Warning

Do not deploy this repository as a public internet-facing service without additional hardening such as:

- authentication and authorization
- rate limiting
- stricter input validation
- sandboxing for file handling
- deployment-specific secrets management