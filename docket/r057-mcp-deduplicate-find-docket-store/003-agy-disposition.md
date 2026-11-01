---
protocol: docket/0.3
id: r057/003-agy
docket: r057
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket-mcp, python3 tools/docket-test: 200 checks / 0 failing]
date: 2026-11-01T21:00:42Z
---

# Resolved: deduplicated find_docket_store() in docket-mcp

Verified in commit c9eb7b9 and T36. `call()` now passes the resolved `found_st` and normalized `docket` id to `run_new()` without mutating caller arguments, eliminating the second lookup.
