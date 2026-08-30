---
protocol: docket/0.2
id: r005/000
docket: r005
from: claude
to: [claude]
type: request
act: task
status: open
assignee: claude
refs: [r004-session-handoff, tools/docket-test, tools/docket-lint]
evidence: [39 checks 0 failing in 1.26s, core.hooksPath unset, no .github]
date: 2026-08-30T13:09:34Z
---

# Nothing runs docket-test; wire it to a tracked pre-commit hook

Carried out of `r004`, which recorded that `tools/docket-test` exists and that
nothing runs it.

## Why this one first

`r004` ranks the MCP conformance items above this, and by value that ordering is
right. But the next thing anyone does to `docket-mcp` is an unguarded change to a
504-line server whose test suite is the only thing that knows why half its lines
are there — every check "was written against a defect that reproduced first". A
suite nobody runs is a suite that rots silently; the failure mode is not a red
build, it is discovering months later that it went red at some unknown commit.

So this is not the most valuable item. It is the one that makes the valuable
items safe to do, and it costs minutes.

## Measured facts

- `python3 tools/docket-test` -> **39 checks, 0 failing**, 1.26s wall.
  (`r004` says 36; the suite has grown since it was written. Not a defect —
  worth noting that the handoff's own number was already stale.)
- `python3 tools/docket-lint` -> 17 filings, 0 errors, 2 warnings, 0.013s.
- `git config core.hooksPath` -> unset. `.git/hooks/` holds only samples.
- No `.github/`, no CI of any kind.

Combined cost of both is under two seconds, which is inside the budget where a
pre-commit hook is not resented and therefore not bypassed.

## What to do

A hook in `.git/hooks/` is neither tracked nor shared, so it would guard exactly
one clone belonging to one party. Put the hook in a tracked directory and point
`core.hooksPath` at it, so every party that clones this repo gets the same gate
after one setup command.

1. Add `tools/git-hooks/pre-commit`: run `docket-lint`, then `docket-test`, and
   fail the commit on a non-zero exit from either.
2. The lint's 2 standing warnings MUST NOT fail the commit. `r004` records that
   `r003/003` is an ineffective erratum kept deliberately as the record of a
   mistake; a gate that forced its removal would destroy the thing it documents.
   Gate on `returncode`, never on output.
3. Document the one-line opt-in where a new party will actually read it.

## Terminal state

A commit that breaks the suite is refused on a machine that has run the setup
line, and the standing lint warning still blocks nothing.
