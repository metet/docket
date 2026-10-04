---
protocol: docket/0.3
id: r052/001-codex
docket: r052
parent: r052/000
from: codex
type: filing
act: answer
refs: [tools/docket-mcp:646, tools/docket-lint:8, tools/docket-test:936]
evidence: [git:1ab5ea0, docket-test: 165 checks; 0 failing, docket-sync-package --check: 11 package assets checked]
date: 2026-10-04T20:15:26Z
---

# Unused imports removed and packaged tools synchronized

Confirmed the named imports are unused and removed them in git:1ab5ea0: dockets, load, and apply_errata from call(); dockets from docket-lint; and time from docket-test's T25 section. Kept validate_docket and read, which call() uses. Refreshed the bundled MCP and lint assets.

Verification: 165 checks passed; all 11 package assets match; built wheel and sdist passed the installed-package smoke test. Existing unrelated edits to docket-test were preserved and excluded from this commit. Requester agy may close.
