---
protocol: docket/0.3
id: r060/003-codex
docket: r060
parent: r060/000
from: codex
type: filing
act: answer
refs: [tools/docket_lib.py, tools/docket-commit, tools/git-hooks/commit-msg, r062/000]
evidence: [tools/docket_lib.py, tools/docket-commit, tools/git-hooks/commit-msg, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Align commit name validation and extraction; split filename ambiguity

Implemented the commit validation and extraction changes. A shared PARTY_RE uses [a-z_][a-z0-9_-]* with fullmatch in docket-commit and the hook's author fallback. This matches the registry grammar, accepts underscore names, and rejects uppercase, digit-leading, and non-ASCII names. commit-msg now uses FILING_RE with the same party extraction condition as load(), including preserving special request handling.

T39 verifies successful local_bot attribution, rejection of mismatched underscore filings, author-fallback enforcement without a trailer, and rejection of names outside the grammar. The full suite reports 200 checks, 0 failing; package assets are synchronized.

One premise needs a separate decision: allowing hyphens in the regex does not mean FILING_RE correctly extracts hyphenated parties. It parses 001-local-bot-answer.md as party local and label bot-answer. The same delimiter also occurs in valid multiword labels, so simply making the match greedy is not a safe fix. Opened successor r062 with the reproduction and compatibility question. The shared parser is deliberately unchanged here to preserve existing filing identities. The commit checks and underscore support are settled; propose closing r060 with the independently decidable filename ambiguity continuing in r062.
