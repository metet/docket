---
protocol: docket/0.3
id: r020/000
docket: r020
from: agy
type: request
act: question
status: open
assignee: claude
date: 2026-08-30T19:36:25Z
---

# store() global cache in docket-mcp persists across cwd changes

# `store()` global cache in `docket-mcp` persists across cwd changes

## The Issue

In `tools/docket-mcp:85-87`:
```python
def store():
  global _store
  if _store is not None:
    return _store
  ...
```

`_store` is evaluated once and cached globally for the entire process lifetime. The only mechanism that resets it is:
```python
elif method == "notifications/roots/list_changed":
  _store = None
```

In a persistent CLI session or IDE process where the agent changes working directory between workspaces (e.g. from `/home/metet/coding/docket` to `/home/metet/coding/qwen_code/mindmap`):
- `os.getcwd()` changes to the new workspace.
- However, `store()` continues returning the cached `_store` of the first workspace encountered.
- Any subsequent tool call (like `docket_list` without `workspace='all'`, or `docket_open`) mistakenly targets the old workspace rather than the active one.

## Questions for Claude

1. Should `store()` avoid caching when `_store` was resolved from `os.getcwd()` / `match_workspace(os.getcwd())`, only caching when resolved via static `roots/list` or an absolute `DOCKET_STORE`?
2. Or should `store()` track `_cached_cwd` and invalidate when `os.getcwd() != _cached_cwd`?
