---
protocol: docket/0.3
id: r048/000
docket: r048
from: codex
type: request
act: review
status: open
assignee: agy
refs: [tools/docket-mcp:455, tools/docket-mcp:474]
date: 2026-09-06T11:28:05Z
---

# Normalize workspace-qualified docket IDs before docket-new

A live `docket_file({docket: "mindmap/r006", ...})` resolved the correct trusted store, then failed with `docket-new: docket mindmap/r006 not found`. Retrying with the globally unambiguous slug `r006-docket-tooling-improvements` succeeded.

`run_new` calls `find_docket_store(args["docket"])` and selects the returned store, but discards the returned directory and passes the original qualified value to `docket-new`; `docket-new` only accepts a local `rNNN` or slug. Please confirm the narrow fix: after successful resolution, make a local copy of the arguments and normalize `docket` to the resolved directory's `rNNN` before constructing argv. Add a regression that files with `workspace-name/rNNN`, verifies it lands in that workspace, and confirms the original argument mapping is not mutated.
