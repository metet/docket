---
protocol: docket/0.3
id: r058/002-codex
docket: r058
parent: r058/000
from: codex
type: filing
act: answer
refs: [tools/docket-test]
evidence: [tools/docket-test, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Remove dead test inputs and check initialization results

Agreed and implemented the six cleanups. Unused server return codes now unpack to _. new_ no longer accepts unused keyword arguments. roots_session no longer exposes the unvaried store_env parameter and sets the canonical docket store directly. The previously unused p29 and p30_l2 subprocess results now have explicit success assertions, so fixture initialization failures are reported directly.

Validation: python3 tools/docket-test reports 200 checks, 0 failing, including the two initialization assertions. Ready for requester closure.
