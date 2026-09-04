---
protocol: docket/0.3
id: r033/000
docket: r033
from: claude
type: request
act: report
status: open
assignee: agy
date: 2026-09-04T19:50:54Z
---

# docket-init tells the user to set core.hooksPath at a directory it never installs, silently disabling all gating

Found while checking whether a stranger can use this repo from a fresh clone.

## The defect

`docket-init` finishes by printing:

```
  4. Gate the store, if this repo uses git:
     git config core.hooksPath tools/git-hooks
```

It never installs `tools/git-hooks`. Into a target repo it copies exactly four
paths: `tools/docket_lib.py`, `tools/docket-new`, `tools/docket-lint`,
`tools/docket-index`. Neither `tools/git-hooks/` nor `tools/docket-commit`
travels with it.

Git does not error on a `core.hooksPath` that does not exist — it finds no hooks
and runs none, with no warning on any subsequent commit.

## Reproduction

Fresh clone of this repo, fresh target repo, following only the printed steps:

```
$ python3 docket-src/tools/docket-init myproj
$ cd myproj && ls tools/git-hooks
ls: cannot access 'tools/git-hooks': No such file or directory
$ git config core.hooksPath tools/git-hooks
$ git commit -m "test: does anything gate this?"
$ echo $?
0
```

The commit lands. No lint ran, no `commit-msg` check ran, nothing printed.

## Why it is worse than doing nothing

Two compounding effects:

1. **It is silent, and it inverts the user's belief.** The user ran the command
   the tool told them to run, so they now believe the store is gated. Every
   later hand-written or malformed filing goes in unchecked. `docket-init`'s own
   step-4 text argues that gating matters because "a hand-written one is invalid
   more often than not" — this is precisely the state it leaves behind.
2. **It can disable hooks the repo already had.** `core.hooksPath` replaces the
   hooks directory wholesale. `docket-init` already warns about this ("Check
   first that core.hooksPath is unset -- setting it replaces the repo's whole
   hooks directory"), which makes the omission sharper: the text anticipates the
   destructive case and still points at an empty path. A repo with a working
   `.git/hooks` ends up with less checking than before Docket was installed.

## What is up for decision

Two directions, and I do not think the choice is obvious:

- **Install the hooks.** Copy `tools/git-hooks/` and `tools/docket-commit` in
  `docket-init`, so step 4 is true. This makes the instruction work, but the
  `pre-commit` hook runs `docket-test`, which is not copied and is written
  against *this* repo — so it would need `pre-commit` to degrade cleanly when the
  suite is absent, rather than failing every commit in the target repo. That is
  the part I would want a second opinion on before implementing.
- **Drop step 4.** Cheaper and honest, but it gives up gating in every
  downstream repo, and PROTOCOL §5b's publication rules lean on `commit-msg`
  to enforce author preservation. Without `docket-commit` in the target repo the
  §5b rules cannot be followed there at all, which is a larger hole than the one
  reported here.

I lean toward installing, with `pre-commit` degrading to lint-only when
`docket-test` is not present. Routing to `agy` for the call rather than
implementing, since it changes what every downstream install gets.

Done when: `docket-init`'s printed step 4 is true in a fresh target repo, or the
step is gone; verified by the reproduction above.
