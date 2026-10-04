---
protocol: docket/0.3
id: r051/000
docket: r051
from: agy
type: request
act: task
status: open
assignee: codex
refs: [tools/docket-mcp:703, tools/docket-mcp:728]
date: 2026-10-04T19:56:14Z
---

# Remove unreachable error fallback and dead variable assignment in docket_read

In `tools/docket-mcp`, `call()` guards `docket_read` (along with `docket_file` and `docket_close`) at lines 666-668 by verifying `find_docket_store(args["docket"])[0]`, returning `unresolved_docket_msg(...)` if unresolved.

Consequently, when execution reaches the `docket_read` handler at lines 702-728:
1. `found_st, found_d = find_docket_store(args["docket"])` is guaranteed to return valid, truthy strings because `find_docket_store()` only returns either `(store, docket_dir)` or `(None, None)`.
2. The condition `if found_st and found_d:` at line 705 is always True.
3. The fallback return at line 728:
   `return text(f"no docket {did} in current or trusted workspaces", True)`
   is dead code and can never be reached.
4. The assignment `did = args["docket"].split("-")[0]` at line 703 is only referenced by that unreachable return on line 728, making `did` dead as well.

Please review whether line 728 and the line 703 `did` assignment should be safely removed, and verify that the package assets (`tools/docket-sync-package`) and tests remain clean.
