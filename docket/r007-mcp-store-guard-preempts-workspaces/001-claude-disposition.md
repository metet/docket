---
protocol: docket/0.2
id: r007/001-claude
docket: r007
from: claude
type: disposition
status: resolved
refs: [tools/docket-mcp:355-395, tools/docket-test:T17, tools/docket-test:T14]
evidence: [48 checks 0 failing; docket_read/docket_file/docket_list all succeed from cwd=/home/metet/coding/qwen_code]
date: 2026-08-30T13:25:05Z
---

# Named dockets now resolve by id from any cwd; docket_open alone still needs a local store

Resolved as specified. All four points of the request are done.

## What changed

The blanket guard is replaced by per-tool resolution in `call()`:

- `docket_read`, `docket_file`, `docket_close` resolve through
  `find_docket_store` first and fail only when the id matches nothing anywhere.
- `docket_list` with no local store degrades to `workspace="all"` instead of
  erroring. What a party owes is the one question the store must always be able
  to answer, and answering it must not depend on which directory the client
  happened to start in.
- `docket_open` keeps the guard. It names no docket, so nothing disambiguates it,
  and the request was explicit that guessing is not allowed: a docket opened in
  the wrong store is a write no later filing can take back. The message now lists
  the trusted workspaces that do have a store and says it will not choose.

Verified from `cwd=/home/metet/coding/qwen_code`, which holds no store:

| call | before | after |
| --- | --- | --- |
| `docket_list {}` | fails | lists both workspaces |
| `docket_read r008` | fails | reads it |
| `docket_read mindmap/r002` | fails | reads it |
| `docket_read r999` | fails, wrong reason | names the id and where it looked |
| `docket_open` | fails | still fails, now naming the alternatives |

Six checks added as `T17`, including that `docket_open` still refuses — the point
is not that everything now works, it is that the one genuinely ambiguous call
still does not.

## A second defect, found by the fix

`T14` began failing. Not a regression: two of its checks asserted that
`docket_list` errors without a store, which is exactly the behaviour this docket
changed. They now run against `docket_open`, which still carries that contract.

Underneath that, `T14` was reading **the developer's real workspace allowlist**.
It never set `DOCKET_WORKSPACES_FILE`, so the server found `~/coding/docket`
trusted on this machine and returned live dockets into a test that expected an
error. The checks passed before only because the old guard failed the call
regardless of workspaces, which hid the leak. `T14` is now pinned to an empty
allowlist.

That is worth stating plainly: **the suite's result depended on local machine
state**, in a repo where the suite is the only record of why the server looks the
way it does. It is fixed here rather than deferred to its own docket because it
was `T14`'s own setup, not a separate component — but the rest of the suite has
not been audited for the same class of leak, and `T15` builds its own allowlist
correctly while `T14` did not, which suggests the pattern was known and simply
missed once.

Suite: **48 checks, 0 failing** (was 42).

## Not addressed

`r008` — that a docket can be open and owed by nobody — is untouched and remains
the more consequential of the two, because it decides whether an open docket is
ever seen again.
