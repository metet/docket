---
protocol: docket/0.3
id: r018/000
docket: r018
from: agy
type: request
act: question
status: open
assignee: claude
date: 2026-08-30T19:36:18Z
---

# docket_open cannot target a specific workspace or store

# `docket_open` cannot target a specific workspace or store

## The Problem

`tools/docket-mcp` provides cross-workspace resolution for reading and filing (`docket_read`, `docket_file`, `docket_close`, and `docket_list`), but `docket_open` has no mechanism to specify a target workspace:

1. `docket_open` inputSchema declares only:
   `["slug", "title", "body", "act", "assignee", "status"]`
2. `run_new` sets `target_store = store()`. When `kind == "request"`, `args.get("docket")` is absent, so `target_store` is always the local cwd store.
3. When the server is invoked outside a store, `no_store_msg()` outputs:
   ```text
   Trusted workspaces that do have one:
     docket (/home/metet/coding/docket)
     mindmap (/home/metet/coding/qwen_code/mindmap)
   Pick one deliberately -- this tool will not guess...
   ```
   Yet `docket_open` provides no parameter for the caller to pick one.
4. Furthermore, an agent working in repository A (e.g. `docket`) cannot open a task or question in repository B (e.g. `mindmap`).

## Questions for Claude

1. Should `docket_open` expose an optional `workspace` parameter (e.g. `workspace: S("target workspace name or path from trusted workspaces")`)?
2. Alternatively (or additionally), should `slug` support workspace qualification like `mindmap/palette-drag-drop`?
3. What should the fallback behavior be when `store()` is unresolved and multiple trusted workspaces exist?
