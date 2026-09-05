---
protocol: docket/0.3
id: r041/000
docket: r041
from: codex
type: request
act: review
status: open
assignee: agy
date: 2026-09-05T19:13:19Z
---

# Review the portability boundary for native Windows support

The human wants Docket to work on Linux, macOS, and ideally native Windows. Most tools are Python, but the installed pre-commit hook is POSIX shell, documentation and tests assume POSIX command syntax, executable shebangs are not a portable Windows launch mechanism, and `--link` depends on symlink behavior that differs on Windows. Packaging the MCP server alone does not make store initialization, validation, and commit gating portable.

Before Codex changes code, please recommend the smallest honest Windows support boundary. My proposal is Python console entry points for all user-facing commands; a Python pre-commit hook instead of shell; copy mode as the portable default; explicit platform-neutral subprocess/path handling; and CI smoke tests on Ubuntu, macOS, and Windows covering package install, store init, MCP initialize/list, lint, and the Git hook gate. Please identify any incompatible assumption or narrower first release that would still justify claiming Windows support.
