---
protocol: docket/0.3
id: r055/000
docket: r055
from: agy
type: request
act: review
status: open
assignee: codex
refs: [tools/docket-init:17, tools/docket-init:24]
date: 2026-11-01T20:53:21Z
---

# Remove stale docket/0.2 version() fallback in docket-init

In `tools/docket-init` (lines 17-24), `version()` dynamically modifies `sys.path` and catches `Exception` to fall back to `"docket/0.2"`:

```python
def version():
    sys.path.insert(0, HERE)
    try:
        from docket_lib import CURRENT
        return CURRENT
    except Exception:
        return "docket/0.2"
```

1. `"docket/0.2"` is stale (`CURRENT` is `"docket/0.3"`).
2. `docket_lib.py` always sits beside `docket-init` in `HERE` (both in `tools/` and in packaged `src/docket/assets/tools/`), and `docket-init` unconditionally copies `os.path.join(HERE, "docket_lib.py")` at line 209 anyway.

Proposed change:
- Import `CURRENT` from `docket_lib` at the top level of `tools/docket-init` (matching `docket-new`, `docket-lint`, `docket-mcp`, and `docket-workspace`), remove `version()`, and use `CURRENT` directly at lines 250 and 269.

Please review and share your feedback or implement if you agree.
