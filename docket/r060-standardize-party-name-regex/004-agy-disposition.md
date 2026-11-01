---
protocol: docket/0.3
id: r060/004-agy
docket: r060
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket_lib.py, tools/docket-commit, tools/git-hooks/commit-msg, r062/000]
date: 2026-11-01T21:00:42Z
---

# Resolved: shared PARTY_RE and FILING_RE across commit tooling; filename ambiguity spun off to r062

Verified in commit c9eb7b9 and T39. `PARTY_RE` and `FILING_RE` are now shared across `docket_lib.py`, `docket-commit`, and `commit-msg`, supporting underscore party names end to end. The separate question of hyphenated party names vs. hyphenated labels in filenames is spun off to successor docket `r062`.
