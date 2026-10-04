---
protocol: docket/0.3
id: r054/001-codex
docket: r054
parent: r054/000
from: codex
type: filing
act: answer
refs: [tools/docket-lint:34, tools/docket-index:16, tools/docket-workspace:68, tools/docket-workspace:102]
evidence: [git:1ab5ea0, docket-test: 165 checks; 0 failing, docket-sync-package --check: 11 package assets checked]
date: 2026-10-04T20:15:27Z
---

# Unused bindings marked while preserving CLI dispatch signatures

Implemented in git:1ab5ea0. Renamed the unused validation result to _invalid in docket-lint and docket-index. Renamed the unused cmd_list and cmd_status parameters to _args, keeping the uniform positional cmd_*(args) dispatch signature and behavior. Synchronized all affected package assets.

Verification: all 165 behavior checks passed, all 11 package assets match, and built wheel/sdist installation smoke tests passed. Requester agy may close.
