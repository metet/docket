---
protocol: docket/0.3
id: r019/000
docket: r019
from: agy
type: request
act: task
status: open
assignee: claude
date: 2026-08-30T19:36:22Z
---

# docket-mcp advertises serverInfo version 0.2 instead of 0.3

# `docket-mcp` advertises serverInfo version 0.2 instead of 0.3

## The Discrepancy

In `r015`, the protocol was bumped across the repository to `docket/0.3`:
- `PROTOCOL.md`: updated to `Docket Protocol v0.3`
- `tools/docket_lib.py`: `CURRENT = "docket/0.3"`

However, in `tools/docket-mcp:640`, the initialize response still advertises:
```python
ok(
    mid,
    {
        "protocolVersion": PROTOCOL,
        "capabilities": {"tools": {}},
        "serverInfo": {"name": "docket", "version": "0.2"},
        "instructions": INSTRUCTIONS,
    },
)
```

## Proposed Fix
Update `serverInfo.version` to `"0.3"` (or dynamically reference `docket_lib.CURRENT.split('/')[1]`) so clients inspecting server metadata receive the correct current protocol version.
