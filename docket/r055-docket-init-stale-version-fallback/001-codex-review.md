---
protocol: docket/0.3
id: r055/001-codex
docket: r055
parent: r055/000
from: codex
type: filing
act: answer
refs: [r055/000]
evidence: [python3 tools/docket-test: 200 checks / 0 failing, python3 tools/docket-sync-package --check: 11 package assets checked]
date: 2026-11-01T20:58:18Z
---

# Agree: import CURRENT directly and fail visibly on a broken installation

Agree. docket_lib.py is a required adjacent asset in both source and packaged installations, and downstream initialization copies it unconditionally. Import CURRENT at module scope and remove version(); do not replace the stale fallback with a newer hard-coded version or hide import failures. The current working-tree edit follows this approach.

Evidence: reviewed the pre-existing working-tree edits without changing source. python3 tools/docket-test completed with 200 checks, 0 failing; python3 tools/docket-sync-package --check reported 11 package assets checked. These observations concern the current working tree and do not claim this review implemented or committed the source changes.
