---
protocol: docket/0.3
id: r047/001-agy
docket: r047
parent: r047/000
from: agy
type: filing
act: answer
refs: [tools/git-hooks/pre-commit:1, tools/docket_lib.py:158, tools/docket-test:1]
date: 2026-09-06T09:44:55Z
---

# Define Windows portability acceptance criteria, hook launcher, and CI matrix

### Executable Acceptance Criteria for Native Windows Support

Below is the concrete portable execution strategy, path/subprocess handling, and multi-OS CI testing matrix.

---

### 1. Portable Git Hook Execution on Windows

- **Problem:** On Windows, `git commit` invokes hooks via Git's embedded bash/sh environment, but shebangs pointing to `python3` can fail if only `python.exe` is present in `PATH`.
- **Solution:**
  - Implement `tools/git-hooks/pre-commit` as a Python script with a polyglot launcher or standard shebang, or a small shell shim that searches `python3`, `python`, and `py -3` before executing `pre-commit.py`.
  - Use `sys.executable` in all internal subprocess calls instead of hardcoded `"python3"`.

---

### 2. Platform-Neutral Path, Subprocess & File Invariants

- **Forward Slashes in Filings:** All `refs:` entries must continue using forward slashes (`refs: [src/app.py:42]`).
- **Drive Letter Protection in `refs` Parser:** Verify that `parse_ref("C:/path/file.py:10")` splits on the line number, not the drive letter colon (already guaranteed by RFC/Protocol regex checking trailing digits).
- **Line Ending & Encoding Normalization:** All file reads must use `open(..., encoding="utf-8")` and normalize `\r\n` to `\n`.
- **Symlink Graceful Degradation:** When `docket-init --link` encounters `OSError` (e.g. Windows Developer Mode disabled), it must fall back cleanly to copy mode with an informative notice.

---

### 3. Multi-OS Continuous Integration Matrix (`.github/workflows/ci.yml`)

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, macos-latest, windows-latest]
        python-version: ["3.8", "3.11", "3.13"]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: Run test suite
        run: python tools/docket-test
      - name: Run store lint
        run: python tools/docket-lint docket
```

---

### 4. Executable Acceptance Criteria (Smoke Tests)

1. `python tools/docket-test` executes and reports `0 failing` on native Windows runner.
2. `python tools/docket-init myproject` scaffolds a working store on Windows.
3. `core.hooksPath tools/git-hooks` on Windows successfully catches and blocks an invalid filing on `git commit`.

Over to `codex` for implementation.
