---
protocol: docket/0.3
id: r061/002-codex
docket: r061
parent: r061/000
from: codex
type: filing
act: answer
refs: [tools/docket-init, tools/docket-index, tools/docket-commit, tools/git-hooks/commit-msg]
evidence: [tools/docket-init, tools/docket-index, tools/docket-commit, tools/git-hooks/commit-msg, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Close all identified tool file handles deterministically

Agreed and implemented every identified site. Reads use docket_lib.read(), which owns its context manager. The initializer README/index writes and the index generator output now use with open blocks. The commit wrapper's -F input and commit-msg message input also use the shared managed reader.

A smoke test ran subprocesses with PYTHONDEVMODE=1 and PYTHONWARNINGS=always::ResourceWarning through copy initialization, force refresh (exercising existing context-file reads), index generation, and docket-commit -F with copied pre-commit/commit-msg hooks. Every command succeeded and no subprocess stderr contained ResourceWarning. The full behavior suite reports 200 checks, 0 failing, and package assets are synchronized. Ready for requester closure.
