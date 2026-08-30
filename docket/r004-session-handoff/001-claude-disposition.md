---
protocol: docket/0.2
id: r004/001-claude
docket: r004
from: claude
type: disposition
status: resolved
refs: [r005-test-harness-runs, r006-mcp-initialize-instructions]
evidence: [42 checks 0 failing, tools/git-hooks/pre-commit, tools/docket-mcp instructions field]
date: 2026-08-30T13:13:00Z
---

# Threads picked up: r005 resolved, r006 open; the rest stay deferred, now with reasons

Resolved. The terminal state was a later session picking the threads up; this is
that session. Two dockets opened, one resolved, one open. What follows is what
was chosen and — more usefully — what was not, and why, so the next party does
not re-derive the same triage.

## Picked up

**`r005` — nothing runs `docket-test`. Resolved.** A tracked `pre-commit` hook
now gates lint and suite, verified by seeding a break and watching the commit be
refused. Taken first not because it is the most valuable item but because it is
the precondition for touching a 504-line server whose test suite is the only
record of why half its lines exist.

**`r006` — `initialize.instructions`. Open, blocked.** The field is sent and
covered by three new checks; whether any installed host surfaces it is unverified,
and this session cannot verify it because it negotiated its own handshake before
the change. Left open deliberately rather than closed on the code change.

## Not picked up, with reasons

**The rest of the MCP conformance list.** `resources` and `resources/subscribe`,
`prompts`, `outputSchema`, `completion/complete`. `r004`'s value ordering still
looks right and `resources` is the obvious next one — stable URIs are what a store
of immutable filings is for. The `2025-03-26` bump stays deferred on the batching
audit `r004` describes; nothing learned here changes that.

**`PARTIES.md` context budgets.** Still `unverified` for `codex`, `agy` and
`openclaw`. Not filled in, because the file forbids guessing one and this session
had no way to establish them that was better than guessing. That is the whole
blocker: it is a small research task for whoever can run those CLIs and read their
configs, not a judgement call. `openclaw` still has no `mcp` subcommand.

**BRD Q1-Q5.** Deferred at least twice already, and `r004` is right that Q2 and Q3
are effectively answered — by `r003` and by the accident of this repo's own layout.
Worth ten minutes of recording, worth nothing more, and it was not the best use of
this session.

**A defect found while working, not filed as its own docket.** `docket_open` and
the other writes fail when the client's cwd is not itself a store, even though
`docket_list` and `docket_read` transparently reach trusted workspaces: writes
have no workspace fallback, so the first call of this session returned "no docket
store at .../qwen_code/docket". Everything here was filed through `tools/docket-new`
instead. Real, reproducible, and someone should open a docket for it — this
disposition is not the place to decide the fix.

## The flowboard threads: do not fix them

`r004` lists two bugs in `~/coding/qwen_code/mindmap` — `input.js:14` and
`input.js:74-75` — as open threads. **They are not to be fixed.** That repo is a
running experiment in what a small local model produces unaided, and repairing the
code destroys the evidence the experiment exists to collect. This is a standing
instruction from `human`, and it outranks the invitation in `r004`'s own text.

Note also that `mindmap/r002-palette-drag-drop` is open, filed by `qwen`, assigned
to `codex`, and its coordinate-math question is the same defect as `input.js:74-75`
— found by review here before `qwen` hit it in use. That docket belongs to `codex`.
Observation is in scope; edits are not.

## Correction carried forward

`r004`'s evidence field records 36 checks. The suite was at 39 when this session
started and is at 42 now. Nothing regressed; the number was stale on the day it
was written, which is the argument for `r005` stated in one line.
