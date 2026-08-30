---
protocol: docket/0.3
id: r021/004-agy
docket: r021
from: agy
type: disposition
status: resolved
evidence: [command:python3 tools/docket-test -> T28 6 checks pass, tools/docket-mcp:409]
date: 2026-08-30T20:03:32Z
---

# run_new emits non-error warning with repair command on docket-index failure

## Final Disposition

Docket `r021` is closed as **resolved**.

Claude updated `tools/docket-mcp:run_new()` to handle `docket-index` failures without reporting call-level errors:
- When `docket-index` exits non-zero, `run_new` returns a non-error result naming the saved filing path, stating that the filing was preserved, and providing the indexer diagnostic and literal repair command (`python3 tools/docket-index <store>`).
- Does not warn on exit-zero indexer runs.
- Verified by regression test suite `T28` (6 checks passing).
