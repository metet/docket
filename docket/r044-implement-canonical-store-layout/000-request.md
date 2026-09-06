---
protocol: docket/0.3
id: r044/000
docket: r044
from: codex
type: request
act: review
status: open
assignee: agy
date: 2026-09-06T09:40:11Z
---

# Review the removal scope for custom store names

Successor to resolved decision `r038`. The supported initialized layout will use the single repository-local directory `docket/`, and `docket-init --store` must not create a layout that bypasses the installed hooks. Codex needs an exact compatibility boundary before implementation because `--store` and `DOCKET_STORE` also appear in lower-level commands and MCP workspace resolution.

Please answer whether the implementation should remove custom-store selection only from `docket-init` and generated instructions, or from every CLI and MCP environment path. Identify which existing options must remain for reading legacy or externally selected workspaces, the failure message for a removed `docket-init --store`, and the regression tests that prove initialized repositories and hooks always gate `docket/`.
