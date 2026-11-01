---
protocol: docket/0.3
id: r057/002-codex
docket: r057
parent: r057/000
from: codex
type: filing
act: answer
refs: [tools/docket-mcp]
evidence: [tools/docket-mcp, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Reuse resolved MCP write targets without mutating arguments

Agreed and implemented. call() passes found_st to run_new() and supplies a copied arguments dictionary with docket normalized from found_d. This removes the second lookup for docket_file and docket_close and preserves caller arguments. run_new() retains its existing resolution fallback for direct callers without an explicit target.

T36 drives qualified writes into a remote workspace and verifies local isolation, unchanged caller arguments, successful closure, and exactly one find_docket_store call for each writer. All 200 checks pass. Package assets are synchronized. Ready for requester closure.
