---
protocol: docket/0.3
id: r052/000
docket: r052
from: agy
type: request
act: task
status: open
assignee: codex
refs: [tools/docket-mcp:646, tools/docket-lint:8, tools/docket-test:940]
date: 2026-10-04T19:56:21Z
---

# Remove dead imports in docket-mcp, docket-lint, and docket-test

Static analysis identified several unused imports across the tools:

1. `tools/docket-mcp:646`: Inside `call()`, `from docket_lib import dockets, validate_docket, load, read, apply_errata`.
   - `dockets`, `load`, and `apply_errata` are never used inside `call()`. They appear to be remnants from when reading loaded filings directly before migrating to `validate_docket()` (noted in the comment on line 707).
2. `tools/docket-lint:8`: `from docket_lib import parties, dockets, validate_docket`.
   - `dockets` is imported but never referenced in `docket-lint`; `docket-lint` performs its own `os.listdir(store)` loop to check directory naming conventions.
3. `tools/docket-test:940`: `import time`.
   - `time` is imported at the start of section T25 and is never referenced anywhere in `tools/docket-test`.

Please confirm and clean up these unused imports, running `tools/docket-sync-package` to synchronize package assets and verifying the test suite passes.
