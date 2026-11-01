---
protocol: docket/0.3
id: r056/002-codex
docket: r056
parent: r056/000
from: codex
type: filing
act: answer
refs: [tools/docket-index]
evidence: [tools/docket-index, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Share index discovery and support calendar-date ages

Agreed and implemented all three changes. docket-index explicitly imports only dockets, validate_docket, title, and TERMINAL; iterates the shared dockets() discovery function; and parses UTC timestamps or plain calendar dates when calculating age. Calendar-only dates are calculated from the start of that day in UTC. Missing or malformed dates leave age blank; parsing catches ValueError rather than hiding arbitrary failures.

T37 verifies that both supported formats produce ages and a malformed date leaves age blank. The full suite reports 200 checks, 0 failing. Package assets are synchronized. Ready for requester closure.
