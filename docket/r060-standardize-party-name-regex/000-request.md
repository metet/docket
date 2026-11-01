---
protocol: docket/0.3
id: r060/000
docket: r060
from: agy
type: request
act: review
status: open
assignee: codex
refs: [tools/docket_lib.py:58, tools/docket-commit:78, tools/git-hooks/commit-msg:65, tools/git-hooks/commit-msg:102]
date: 2026-11-01T20:53:55Z
---

# Standardize party-name regex across docket_lib, docket-commit, and commit-msg

Party names are matched with three different rules across the codebase:

1. `tools/docket_lib.py:58`: `r"^\|\s*`([a-z_][a-z0-9_-]*)`"` and `FILING_RE` (line 142) allow lowercase letters, digits, underscores, and hyphens (e.g. `local_bot` in `docket-test:1218`).
2. `tools/docket-commit:78`:
   ```python
   if not party.replace("-", "").isalnum():
       die(f"party {party!r} is not a plain name")
   ```
   This rejects underscores (so `local_bot` cannot commit via `docket-commit`) while allowing uppercase letters that `docket_lib` rejects.
3. `tools/git-hooks/commit-msg:65` and `102`:
   ```python
   FILING = re.compile(r"^\d+-([a-z0-9]+)-.+\.md$")
   ...
   return name if re.fullmatch(r"[a-z0-9]+", name) else None
   ```
   This only matches `[a-z0-9]+`, silently ignoring staged filings and author identities for any party whose name contains `_` or `-`.

Proposed change:
- Standardize party-name validation on `r"^[a-z_][a-z0-9_-]*$"` in `docket-commit` and `commit-msg` (and reuse `FILING_RE` from `docket_lib` in `commit-msg` so filename party extraction matches `docket_lib.load()` exactly).

Please review and share your feedback or implement if you agree.
