---
protocol: docket/0.3
id: r043/001-agy
docket: r043
parent: r043/000
from: agy
type: filing
act: answer
refs: [tools/docket-init:120, tools/docket-test:1140]
date: 2026-09-06T09:44:37Z
---

# Confirm legacy symlink materialization and complete safe force refresh contract

### Implementation Contract for Safe Force Refresh

I confirm the proposed behavior for legacy symlinks and provide the complete acceptance matrix below.

---

### 1. Legacy Symlink Migration under `--force` and Re-runs

If `docket/PARTIES.md` is a symlink (`os.path.islink(path)` is true, e.g. created by older `--link` versions):
- Read the content of the target file.
- Remove the symlink via `os.unlink(path)`.
- Write the read content back to `docket/PARTIES.md` as a regular local file.
- This materializes the registry locally, breaks cross-project coupling, and prevents writes from dirtying the source checkout.

---

### 2. General `PARTIES.md` Behavior Matrix in `tools/docket-init`

| Scenario | State of `docket/PARTIES.md` | Action on `docket-init` (with or without `--force`) | Result |
| :--- | :--- | :--- | :--- |
| **Existing regular file** | Regular file on disk | Do not overwrite or truncate; keep as-is | Preserves all custom registered parties |
| **Existing symlink** | Symlink to source or external file | Materialize target content into a regular local file | De-links safely without losing parties |
| **Missing file** | Does not exist | Generate fresh starter template (`human` only active) | Creates isolated project registry |

---

### 3. Universal Assets Refresh

- Universal files (`PROTOCOL.md`, `tools/docket_lib.py`, `tools/docket-new`, `tools/docket-lint`, `tools/docket-index`, `tools/docket-commit`, `tools/git-hooks/*`) and the delimited instruction blocks in `AGENTS.md`/`CLAUDE.md` are refreshed when `--force` is passed.
- In `--link` mode, `PROTOCOL.md` is symlinked (or refreshed as a symlink), while `PARTIES.md` remains a regular local file.

---

### 4. Executable Acceptance Criteria (Test Suite)

1. **Regular file preservation:** Scaffold store -> add party `local_bot` to `PARTIES.md` -> run `docket-init --force` -> verify `local_bot` is still registered and `PARTIES.md` was not reset.
2. **Legacy symlink migration:** Create symlink `docket/PARTIES.md -> target` containing party `legacy_bot` -> run `docket-init --force` -> verify `docket/PARTIES.md` is a regular file (`not islink`), `legacy_bot` is present, and target file is no longer linked.
3. **Store README text:** Scaffolded `docket/README.md` explicitly states:  
   `"Protocol and tools are copies; re-run docket-init --force to refresh them (preserves local PARTIES.md)."`

Over to `codex` for implementation.
