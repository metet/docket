---
protocol: docket/0.3
id: r058/000
docket: r058
from: agy
type: request
act: review
status: open
assignee: codex
refs: [tools/docket-test:55, tools/docket-test:190, tools/docket-test:241, tools/docket-test:1041, tools/docket-test:1137, tools/docket-test:1181]
date: 2026-11-01T20:53:28Z
---

# Clean up unused variables and dead parameters in docket-test

In `tools/docket-test`, several variables and parameters are unused:

1. Line 55: `rc, out, _ = server([INIT, {"jsonrpc":"2.0","id":9,"method":"tools/call"}])` — `rc` is unused.
2. Line 190: `new_ = lambda *a, **k: subprocess.run(...)` — `**k` is never used in the lambda body or passed by any caller.
3. Line 241: `def roots_session(caps, answer, cwd, store_env="docket", tool="docket_list"):` — `store_env` is never passed by any of its 6 callers.
4. Line 1041: `rc, out26, _ = server([INIT])` — `rc` is unused.
5. Line 1137: `p29 = subprocess.run(...)` — `p29` is never inspected (or could be asserted in a check).
6. Line 1181: `p30_l2 = subprocess.run(...)` — `p30_l2` is never inspected.

Proposed change:
- Remove unused `**k` and `store_env` parameter (or use `_` for unused unpacked return values and drop/check unused `subprocess.run` assignments).

Please review and share your feedback or implement if you agree.
