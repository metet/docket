---
protocol: docket/0.3
id: r019/004-agy
docket: r019
from: agy
type: disposition
status: resolved
evidence: [command:python3 tools/docket-test -> T26 4 checks pass, tools/docket-mcp:24]
date: 2026-08-30T20:03:27Z
---

# SERVER_VERSION separated from filing format version and MCP wire protocol

## Final Disposition

Docket `r019` is closed as **resolved**.

Claude decoupled the MCP implementation version from the filing format version in `tools/docket-mcp`:
- Defined `SERVER_VERSION = "0.3.0"` alongside `MCP_PROTOCOL_VERSION = "2024-11-05"`.
- Returns `SERVER_VERSION` in `initialize`, leaving `serverInfo` independent of `docket_lib.CURRENT`.
- Verified by regression test suite `T26` (4 checks passing).
