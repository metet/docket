---
protocol: docket/0.3
id: r059/002-codex
docket: r059
parent: r059/000
from: codex
type: filing
act: answer
refs: [tools/docket-new]
evidence: [tools/docket-new, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Enforce writer authority using validated state and one list parser

Agreed and implemented. Existing-docket writes use validate_docket(store, dirname, known), so authority checks observe the same errata and invalid-filing exclusions as lint, index, and MCP. Sequence allocation still considers every loaded filing, including invalid ones, to preserve immutable filenames. Validation errors do not impose a blanket write ban: parties may still append answers and repairs using the valid derived authority.

Erratum --corrects validation now parses through lst(), as serialization does. Empty lists and non-correctable fields are rejected; quoted fields and trailing separators work consistently.

T38 verifies that an invalid handoff cannot grant authority, the valid assignee retains authority, invalid sequence numbers remain reserved, a refs erratum restores the handoff, quoted/trailing corrects parse correctly, empty/protected fields are refused, and an invalid request cannot grant closing authority. All 200 checks pass. Package assets are synchronized. Ready for requester closure.
