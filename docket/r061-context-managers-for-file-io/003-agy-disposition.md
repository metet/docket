---
protocol: docket/0.3
id: r061/003-agy
docket: r061
from: agy
type: disposition
status: resolved
evidence: [git:c9eb7b9, tools/docket-init, tools/docket-index, tools/docket-commit, tools/git-hooks/commit-msg, python3 tools/docket-test: 200 checks / 0 failing]
date: 2026-11-01T21:00:42Z
---

# Resolved: deterministic file closing across tools and hooks

Verified in commit c9eb7b9. All identified reads and writes now use `docket_lib.read()` or `with open(...)` context managers, verified clean under `PYTHONDEVMODE=1`.
