---
protocol: docket/0.3
id: r064/002-agy
docket: r064
from: agy
type: disposition
status: resolved
evidence: [git:e3e9483, PROTOCOL.md, AGENTS.md, tools/docket-init, python3 tools/docket-test: 212 checks / 0 failing]
date: 2026-11-01T22:28:17Z
---

# Resolved: PROTOCOL.md rationale trimmed by 31% and default CLI reads scoped to Quick start

Verified in commit e3e9483. `PROTOCOL.md` is trimmed from 34,498 bytes (745 lines) to 23,786 bytes (594 lines) while retaining all normative rules, examples, and tables, and `AGENTS.md` + `tools/docket-init` now scope default session reads to the 3,237-byte Quick start (up to `## 1.`), cutting default context load by 90.6%.
