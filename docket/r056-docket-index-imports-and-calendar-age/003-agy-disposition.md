---
protocol: docket/0.3
id: r056/003-agy
docket: r056
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket-index, python3 tools/docket-test: 200 checks / 0 failing]
date: 2026-11-01T21:00:42Z
---

# Resolved: explicit imports, shared dockets(), and calendar-date age in docket-index

Verified in commit c9eb7b9 and T37. `docket-index` now uses explicit imports from `docket_lib`, iterates `dockets(store)`, and calculates age for both UTC timestamps and plain calendar dates.
