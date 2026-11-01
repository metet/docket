---
protocol: docket/0.3
id: r059/003-agy
docket: r059
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket-new, python3 tools/docket-test: 200 checks / 0 failing]
date: 2026-11-01T21:00:42Z
---

# Resolved: write-time authority uses validate_docket() and lst() for --corrects

Verified in commit c9eb7b9 and T38. `docket-new` now derives write-time state via `validate_docket()` while preserving sequence allocation across all filings, and validates `--corrects` through `lst()`.
