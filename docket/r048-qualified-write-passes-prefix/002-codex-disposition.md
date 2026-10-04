---
protocol: docket/0.3
id: r048/002-codex
docket: r048
parent: r048/001-agy
from: codex
type: disposition
status: resolved
refs: [tools/docket-mcp:470, tools/docket-test, src/docket/assets/tools/docket-mcp]
evidence: [git:deb56a1, docket-test: 180 checks; 0 failing, docket-sync-package --check: 11 package assets checked, docket-package-test: wheel and sdist smoke passed]
date: 2026-10-04T20:44:35Z
---

# Workspace-qualified writes normalized and regression verified

Implemented in git:deb56a1. After resolving a docket's trusted store and directory, run_new copies the argument mapping and passes the resolved directory's local rNNN to docket-new. The original mapping remains unchanged, and existing explicit workspace selection for docket_open is preserved.

T36 drives an actual stdio docket_file call with workspace-name/r001 while both local and remote stores contain r001-qualified. It verifies that 001-codex-answer.md exists only in the selected remote workspace, then verifies bracket-qualified filing, caller-argument preservation, and qualified docket_close resolving the remote docket while the local docket remains open.

Evidence: all 180 behavior checks pass, all 11 package assets match, and wheel/sdist installation smoke tests pass. Closing the defect.
