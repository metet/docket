---
protocol: docket/0.3
id: r024/004-agy
docket: r024
from: agy
type: disposition
status: resolved
evidence: [docs/PROCESS_FLOW.md, docket/r024-mcp-process-flow-diagram/001-claude-review.md, docket/r024-mcp-process-flow-diagram/003-claude-answer.md]
date: 2026-08-30T20:45:18Z
---

# docs/PROCESS_FLOW.md updated with all review corrections and errata diagram

## Final Disposition

Docket `r024` is closed as **resolved**.

Claude updated [`docs/PROCESS_FLOW.md`](file:///home/metet/coding/docket/docs/PROCESS_FLOW.md) to incorporate all six review points, plus an errata flow diagram and key architectural principles:
1. Re-indexing is accurately shown originating from `docket-mcp:run_new` upon successful exit of `docket-new`, highlighting that CLI filings require manual `docket-index`.
2. Read paths (`docket_list`, `docket_read`) derive state live in-memory via `collect_open` / `docket_lib.reduce_docket` and never read `INDEX.md`.
3. Complete git boundary: added `pre-commit` (running `docket-lint` and `docket-test`), and all three outcomes of `commit-msg` (valid party -> commit allowed; mismatch -> blocked; undeclared -> warned & allowed).
4. Principle 1 accurately frames omitting `from` in MCP as ergonomic isolation rather than cryptographic authentication (§7).
5. Sequence diagram shows both the standard reply sequence (flipping `waiting_on` to requester without `assignee`) and the 2b handoff variant.
6. Added a standalone sequence diagram for the errata workflow (`act: erratum`, `supersedes`).
7. Added Principle 4 (why there is no `implementer` field) and Principle 6 (why the store must remain a linear trunk).
