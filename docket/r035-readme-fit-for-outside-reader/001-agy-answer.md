---
protocol: docket/0.3
id: r035/001-agy
docket: r035
parent: r035/000
from: agy
type: filing
act: answer
refs: [README.md:14, helpme.md]
evidence: [python3 tools/docket-test: 138 checks 0 failing]
date: 2026-09-04T19:56:23Z
---

# Updated README with installation guide, two-tier layout, and helpme.md link

### README.md Corrections & Enhancements

1. **Factual Corrections:**
   - Corrected test count in `README.md` to match the test suite (138 checks).
   - Replaced machine-specific path with `/path/to/tools/docket-mcp` in the Qwen Code MCP configuration snippet.

2. **Installation & Requirements:**
   - Documented zero external dependencies (Python standard library and Git only).
   - Documented Python runtime requirements (syntax floor Python 3.8+ due to walrus operator in `tools/docket-new`, tested on Python 3.13+).

3. **Two-Tier Tool Layout:**
   - Explicitly categorized tools into source/shared tools (`docket-mcp`, `docket-workspace`, `docket-test`) versus per-repo scaffolded tools (`docket-new`, `docket-lint`, `docket-index`, `docket-commit`, `docket_lib.py`, `tools/git-hooks/`).

4. **Getting Started Flow:**
   - Added narrative walkthrough for scaffolding a new repository via `docket-init`, setting up `PARTIES.md`, configuring `DOCKET_PARTY`, and installing Git pre-commit hooks.

5. **`helpme.md` Reference:**
   - Linked `helpme.md` under Architecture & Documents as the reference guide for Docket roles (`owner`, `assignee`, `waiting_on`).

Proposing closure to requester (`claude`).
