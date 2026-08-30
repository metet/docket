---
protocol: docket/0.2
id: r007/000
docket: r007
from: claude
to: [claude]
type: request
act: task
status: open
assignee: claude
refs: [tools/docket-mcp:355-368, tools/docket-mcp:236-289, r004-session-handoff/001-claude]
evidence: [docket_read r006 isError=true from cwd=/home/metet/coding/qwen_code; docket_file isError=true; docket_list workspace=all succeeds from the same cwd]
date: 2026-08-30T13:17:52Z
---

# The store guard preempts find_docket_store, so most MCP tools fail from a client outside a store

## The defect

`call()` rejects every tool but `docket_protocol` when the client's own working
directory does not contain a store:

```python
if name != "docket_protocol" and not os.path.isdir(store()):
    return text(f"no docket store at {os.path.abspath(store())!r}...", True)
```

`find_docket_store` exists to locate the store that holds a given docket id,
across trusted workspaces, and `run_new` calls it. It is never reached. The guard
runs first and fails the call on the *client's* store, not on the store the
docket argument names — which for `docket_read`, `docket_file` and `docket_close`
is unambiguous, because the id identifies exactly one store.

## Reproduced

Server driven directly with `cwd=/home/metet/coding/qwen_code`, which is not a
store, with `~/coding/docket` and `~/coding/qwen_code/mindmap` both trusted:

| call | result |
| --- | --- |
| `docket_list {workspace: "all"}` | works |
| `docket_protocol` | works |
| `docket_list {}` | fails |
| `docket_read {docket: "r006"}` | fails |
| `docket_open` / `docket_file` / `docket_close` | fail |

`workspace: "all"` works only because its branch sits above the guard. That is the
accident that made the gap look smaller than it is.

## Correcting the record

`r004/001-claude` says "`docket_list` and `docket_read` transparently reach
trusted workspaces". That is wrong. Only `docket_list {workspace: "all"}` does.
`r004` is closed and its filings are immutable, so the correction is recorded here
rather than there. The practical consequence stands: the whole of `r005` and
`r006` was filed through `tools/docket-new`, because the MCP write path could not
be used from the session that did the work.

## What to do

Resolve the target store per call, from the docket argument, before deciding
whether there is a store at all:

1. For `docket_read`, `docket_file` and `docket_close`, let `find_docket_store`
   answer first. Fail only when the id matches nothing in the local store or any
   trusted workspace, and say which id and which workspaces were searched.
2. For `docket_open` there is no id to resolve, so a client outside a store is
   genuinely ambiguous. Keep the guard there, but make the message name the
   trusted workspaces it could have used and how to pick one. Do not guess a
   workspace — opening a docket in the wrong store is a write that cannot be
   taken back.
3. For plain `docket_list`, prefer listing the trusted workspaces over failing.
   A party asking what it owes should not get an error because it happened to
   start in the wrong directory; `waiting_on` is the one question the store must
   always be able to answer.
4. Add checks: each read/write tool reachable by id from a non-store cwd, and
   `docket_open` still refused with a message that names the alternatives.

## Note

This is the defect recorded but not filed in `r004/001-claude`. It is filed now,
with the characterisation corrected.
