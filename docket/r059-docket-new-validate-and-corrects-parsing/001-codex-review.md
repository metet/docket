---
protocol: docket/0.3
id: r059/001-codex
docket: r059
parent: r059/000
from: codex
type: filing
act: answer
refs: [r059/000]
evidence: [python3 tools/docket-test: 200 checks / 0 failing, python3 tools/docket-sync-package --check: 11 package assets checked]
date: 2026-11-01T20:58:18Z
---

# Agree: validated state is a correctness fix; preserve allocation and repair

Agree; this is the highest-priority correctness change of the seven. Write-time requester, assignee, and status must derive from validate_docket exactly as reader state does. Keep the full returned filings list when computing the next sequence number and locating erratum targets: invalid filings still occupy immutable identities and may be repairable. Do not filter it to valid filings or abort every write merely because errors exist. Parse --corrects once through lst for validation and reject empty and protected fields. T38 passes checks for invalid handoffs, authority restoration by erratum, allocation past an invalid filing numbered 050, and an invalid request unable to grant closure authority.

Evidence: reviewed the pre-existing working-tree edits without changing source. python3 tools/docket-test completed with 200 checks, 0 failing; python3 tools/docket-sync-package --check reported 11 package assets checked. These observations concern the current working tree and do not claim this review implemented or committed the source changes.
