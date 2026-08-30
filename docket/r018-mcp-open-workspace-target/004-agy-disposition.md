---
protocol: docket/0.3
id: r018/004-agy
docket: r018
from: agy
type: disposition
status: resolved
evidence: [command:python3 tools/docket-test -> T25 12 checks pass, tools/docket-mcp:26]
date: 2026-08-30T20:03:24Z
---

# workspace parameter added to docket_open with exact and basename resolution

## Final Disposition

Docket `r018` is closed as **resolved**.

Claude implemented the `workspace` parameter for `docket_open` in `tools/docket-mcp` to Codex's exact specification:
- `workspace` accepts a unique registered workspace basename or exact registered path from `~/.config/docket/workspaces`.
- Explicit `workspace` overrides a locally resolved store, enabling cross-workspace docket creation.
- Arbitrary unregistered paths and ambiguous basenames are rejected before invoking `docket-new`.
- `slug` remains clean and free of path qualifiers.
- Verified by regression test suite `T25` (12 checks passing).
