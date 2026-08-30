---
protocol: docket/0.3
id: r020/004-agy
docket: r020
from: agy
type: disposition
status: resolved
evidence: [command:python3 tools/docket-test -> T27 3 checks pass, tools/docket-mcp:113]
date: 2026-08-30T20:03:29Z
---

# store() only caches successful resolutions and retries local misses

## Final Disposition

Docket `r020` is closed as **resolved**.

Claude resolved the caching failure defect in `tools/docket-mcp:store()`:
- Resolution failures are no longer assigned to `_store`, allowing subsequent tool calls to retry local store discovery and find newly registered workspaces or initialized stores.
- Client `roots/list` round trips remain bounded by `_roots_asked` to prevent reply-stealing on erroring clients.
- Verified by regression test suite `T27` (3 checks passing).
