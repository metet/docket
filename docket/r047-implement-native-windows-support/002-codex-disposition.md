---
protocol: docket/0.3
id: r047/002-codex
docket: r047
from: codex
type: disposition
status: resolved
evidence: [git:2d1ca65, url:https://github.com/metet/docket/actions/runs/34029503886, command:python3 tools/docket-test (158 checks; 0 failing)]
date: 2026-09-06T11:13:09Z
---

# Native Linux, macOS, and Windows support is verified

Implemented and verified the portability contract. Both Git hooks are shell/Python polyglots that select Python 3.8+ from `python3`, `python`, or `py -3`, and all internal child processes use `sys.executable`. MCP stdio is explicitly UTF-8; file URIs handle Windows drive paths; protocol reads normalize CRLF; lint-gate paths normalize to the protocol's forward-slash form; `--link` accepts either a symlink or its informative copy fallback; and trusted workspaces resolve macOS path aliases. The CI matrix uses the current `actions/checkout@v7` and `actions/setup-python@v7` releases rather than the obsolete v4/v5 examples in the review. GitHub run 34029503886 passed all nine Ubuntu/macOS/Windows × Python 3.8/3.11/3.13 jobs, including the initialized-repository hook smoke test.
