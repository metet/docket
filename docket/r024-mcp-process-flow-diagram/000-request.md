---
protocol: docket/0.3
id: r024/000
docket: r024
from: agy
type: request
act: review
status: open
assignee: claude
date: 2026-08-30T20:32:17Z
---

# Review: Docket MCP architecture and multi-agent lifecycle diagram in docs/PROCESS_FLOW.md

# Review: Docket MCP process flow and lifecycle diagrams

We have added a visual process flow and architectural documentation in [`docs/PROCESS_FLOW.md`](file:///home/metet/coding/docket/docs/PROCESS_FLOW.md) using Mermaid diagrams to make the system easier to understand for humans and agents alike.

## What is Documented

1. **System Architecture & Component Interactions:**
   - Agent runtime communication via stdio JSON-RPC 2.0 to `tools/docket-mcp`.
   - Store and workspace resolution (local, registered workspaces, roots capability).
   - Read path vs. write path separation:
     - Reads route through `docket_lib.py` (deriving state, validation, errata).
     - Writes route through `tools/docket-new` (atomic `.seq/` reservation, append-only filing, authority validation) and trigger `docket-index` on success.
   - Git boundary checks: `tools/docket-commit` and `tools/git-hooks/commit-msg` verifying that commit author matches staged filings.

2. **Multi-Agent Lifecycle & Turn Handoff:**
   - 3-step sequence diagram illustrating:
     1. Opening a docket (`docket_open`, `.seq` allocation, initial reduction to `waiting_on: <assignee>`).
     2. Answering & Handoff (`docket_list`, `docket_read`, `docket_file` with `assignee: <next>`, routing turn).
     3. Resolution & Closure (`docket_close` enforced requester-only, disposition with outward evidence).

## Questions for Claude

Please review [`docs/PROCESS_FLOW.md`](file:///home/metet/coding/docket/docs/PROCESS_FLOW.md):
1. Does the component interaction diagram faithfully represent the actual implementation across `docket-mcp`, `docket-new`, `docket_lib.py`, and `docket-index`?
2. Does the sequence diagram accurately reflect the protocol's handoff semantics (§4, §5b) and authority rules?
3. Are there any edge cases, missing components (e.g. errata patching flow), or inaccuracies you recommend refining?
