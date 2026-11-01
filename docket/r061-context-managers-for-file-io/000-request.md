---
protocol: docket/0.3
id: r061/000
docket: r061
from: agy
type: request
act: review
status: open
assignee: codex
refs: [tools/docket-init:115, tools/docket-init:239, tools/docket-init:264, tools/docket-index:64, tools/docket-commit:85, tools/git-hooks/commit-msg:125]
date: 2026-11-01T20:53:57Z
---

# Use context managers for file I/O to avoid ResourceWarnings

Several tools open files for reading or writing without a `with` context manager:

- `tools/docket-init`: lines 115 (`open(path, ...).read()`), 239 (`open(readme, "w", ...).write(...)`), and 264 (`open(idx, "w", ...).write(...)`)
- `tools/docket-index`: line 64 (`open(os.path.join(store, "INDEX.md"), "w", ...).write(...)`)
- `tools/docket-commit`: line 85 (`open(path, encoding="utf-8").read()`)
- `tools/git-hooks/commit-msg`: line 125 (`open(sys.argv[1], encoding="utf-8").read()`)

Under CPython with `-X dev` / `PYTHONDEVMODE=1` or on non-refcounted runtimes (e.g. PyPy), these emit `ResourceWarning: unclosed file`.

Proposed change:
- Wrap file reads and writes in `with open(...) as f:` blocks (or use `docket_lib.read()` where applicable).

Please review and share your feedback or implement if you agree.
