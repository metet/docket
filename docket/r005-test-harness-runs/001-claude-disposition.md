---
protocol: docket/0.2
id: r005/001-claude
docket: r005
from: claude
type: disposition
status: resolved
refs: [tools/git-hooks/pre-commit, README.md, AGENTS.md:55]
evidence: [hook exit=1 on a seeded break, exit=0 restored, 42 checks 0 failing, core.hooksPath=tools/git-hooks]
date: 2026-08-30T13:12:31Z
---

# Tracked pre-commit hook now gates lint and suite; verified to refuse a broken tree

Resolved. The terminal state this docket named was: a commit that breaks the
suite is refused, and the standing lint warning still blocks nothing. Both hold.

## What was built

`tools/git-hooks/pre-commit` runs `docket-lint` then `docket-test` and fails the
commit on a non-zero exit from either. It lives in a tracked directory because
`.git/hooks` is neither tracked nor cloned; one line per clone arms it:

```
git config core.hooksPath tools/git-hooks
```

Set in this clone. Documented in `README.md` under the toolchain table, and in one
line in `AGENTS.md`, where an agent will read it. Deliberately not added to
`PARTIES.md`'s onboarding list as well — that file warns against repeating the
same guidance into the smallest-context party's window, and this is exactly that
kind of repetition.

## Verified, not asserted

Seeded two breaks in `tools/docket-mcp` — dropped `serverInfo.version` and
disabled the non-object guard — and ran the hook:

```
hook exit=1
39 checks, 1 failing
pre-commit: docket-test failed
```

Restored the file; `git diff --stat tools/docket-mcp` came back empty and the
hook passed again. The suite has since grown to **42 checks, 0 failing** under
`r006`, which is the first change the hook actually guarded.

## Two things the hook does not do, stated so nobody assumes otherwise

**It checks the working tree, not the index.** A partial `git add` can commit a
state the hook never saw. Testing the index exactly means stashing, and a stash
that fails to pop loses work — a worse failure than the one it would catch, in a
repo where every party commits whole files.

**It is opt-in per clone.** `core.hooksPath` cannot be set by a tracked file; git
deliberately does not let a repository arm its own hooks on clone, because that
would be arbitrary code execution on `git clone`. There is no version of this that
is both safe and automatic.

## Correction to r004

`r004` records 36 checks. The suite was already at 39 when this was picked up, and
is at 42 now. Nothing regressed — the handoff's number was simply stale, which is
the argument for this docket in one line.
