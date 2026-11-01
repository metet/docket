---
protocol: docket/0.3
id: r055/003-agy
docket: r055
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket-init, python3 tools/docket-test: 200 checks / 0 failing]
date: 2026-11-01T21:00:42Z
---

# Resolved: CURRENT imported directly in docket-init

Verified in commit c9eb7b9. `docket-init` now imports `CURRENT` directly from `docket_lib` at module load and removes `version()` and its stale `docket/0.2` fallback.
