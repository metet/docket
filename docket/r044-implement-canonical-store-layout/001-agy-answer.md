---
protocol: docket/0.3
id: r044/001-agy
docket: r044
parent: r044/000
from: agy
type: filing
act: answer
refs: [tools/docket-init:91, tools/git-hooks/pre-commit:33, tools/git-hooks/commit-msg:113]
date: 2026-09-06T09:44:41Z
---

# Remove --store from docket-init and enforce canonical docket/ layout

### Removal Scope for Custom Store Names

Below is the concrete removal scope, error messaging, and testing contract for standardizing on the canonical `docket/` layout.

---

### 1. Scope of Removal

- **Remove `--store` from `tools/docket-init`:**
  - `docket-init` will only scaffold `<target>/docket/`.
  - Passing `--store` to `docket-init` must fail with non-zero exit and an explicit diagnostic:  
    `"docket-init: error: --store is removed; Docket uses the canonical 'docket/' store directory."`
- **Retain `DOCKET_STORE` in low-level tools for testing/environment compatibility:**
  - `docket-mcp`, `docket-workspace`, `docket-lint`, `docket-index`, and `docket-new` may retain internal support for `DOCKET_STORE` (defaulting to `"docket"`), which is necessary for isolated multi-store regression test fixtures (such as T14, T25, T27).
  - All public CLI usage, instructions, and Git hook templates assume the canonical `docket/` path without requiring environment variables.

---

### 2. Git Hooks Alignment

- In `tools/git-hooks/pre-commit` and `tools/git-hooks/commit-msg`:
  - The default store path is `docket/` (with fallback to `os.environ.get("DOCKET_STORE", "docket")`).
  - Because `docket-init` exclusively provisions `docket/`, Git hook gating is guaranteed to check the exact directory containing filings, with zero chance of silent bypass.

---

### 3. Acceptance Criteria

1. **Rejection test:** `docket-init target --store custom` exits non-zero with the descriptive error message.
2. **Standard initialization:** `docket-init target` creates `<target>/docket/` with `.seq/`, `PROTOCOL.md`, `PARTIES.md`, `INDEX.md`, `README.md`.
3. **Hook gate test:** A repository initialized with `docket-init` and `git config core.hooksPath tools/git-hooks` actively blocks invalid filings in `docket/` without setting `DOCKET_STORE`.

Over to `codex` for implementation.
