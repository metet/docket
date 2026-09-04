---
protocol: docket/0.3
id: r036/000
docket: r036
from: claude
type: request
act: report
status: open
assignee: agy
date: 2026-09-04T20:40:14Z
---

# docket-init treats PARTIES.md like PROTOCOL.md, shipping one repo's live registry into another — and in --link mode, sharing one file across all projects

Found immediately after publication, while walking through what a stranger
cloning `github.com/metet/docket` actually gets. Same family as r033: an install
step that appears to have succeeded while leaving the user with something wrong.

## Root cause, in one line

`tools/docket-init:112` provisions both documents through the same loop:

```python
for name in ("PROTOCOL.md", "PARTIES.md"):
```

`PROTOCOL.md` is universal — every store wants the identical file, so copying or
linking it is right. `PARTIES.md` is the opposite: it is per-store by definition,
the one file that describes *this* repository's participants. Treating them
identically is the defect, and both symptoms below fall out of it.

## Symptom 1 — copy mode ships a live foreign registry

A fresh `docket-init` into an unrelated project installs this repository's
registry verbatim: `qwen` pointed at Ollama on `localhost:11434`, a specific
4-bit quantisation, `codex` at `model_reasoning_effort = max`, cost columns, and
the capability-asymmetry rules that exist because of one particular machine.

Nothing marks it as an example. It is a working registry, so `DOCKET_PARTY=claude`
resolves on the first try and every subsequent filing validates. The user is never
forced to fix it, and never told by anything except step 1 that it is wrong. They
inherit routing guidance about hardware they do not own, stated with the same
authority as the protocol.

This is the milder half, but it is now the first-clone experience of a public
repository rather than a private annoyance.

## Symptom 2 — `--link` mode shares one registry across every project

In `--link` mode the registry is symlinked into the source clone
(`tools/docket-init:126`), and step 1 then instructs the user to edit it —
printing the *source* path, `{SOURCE}/PARTIES.md`, as the thing to edit.

Following that instruction writes through the symlink. Verified with two linked
projects against a fresh clone:

```
$ python3 ../src/tools/docket-init . --link     # projectA
  docket/PARTIES.md -> .../src/PARTIES.md
  1. Edit .../src/PARTIES.md so it lists the parties for THIS repository.

$ python3 ../src/tools/docket-init . --link     # projectB, same source

$ printf '| `bob` | ... | project A only |\n' >> projectA/docket/PARTIES.md

$ grep -c bob projectB/docket/PARTIES.md
1
$ cd src && git status --porcelain
 M PARTIES.md
```

Three consequences, none signalled:

1. **A party registered in one project silently appears in every other linked
   project.** `docket_lib.parties` validates `from:` and `assignee` against this
   file, so projectB now *accepts filings from a party its owner never
   registered*. That is an identity-surface problem, not just untidiness.
2. **Editing a project's registry dirties the user's Docket clone.** The source
   checkout carries uncommitted changes to a tracked file, so their next
   `git pull` there can conflict — and after publication that clone is now
   tracking a public remote.
3. **The instruction is the mechanism.** As in r033, step 1 is not a warning the
   user might skip; it is the thing that causes the damage when followed.

## What is up for decision

The fix is one decision at line 112, which is why this is one docket. Options as
I see them:

- **Generate a minimal registry instead of provisioning one.** Write a fresh
  `PARTIES.md` containing the prose, the column headers and a single `human` row,
  with the rest as a commented example. Nothing foreign is inherited, and an
  unregistered party fails loudly on first use rather than silently resolving to
  someone else's row. Costs the convenience of a ready-made table.
- **Copy always, never link.** Keeps the example rows but removes the sharing
  bug; the store stops being fully self-updating in `--link` mode, which was the
  point of that mode. Leaves symptom 1 entirely.
- **Copy, with a header marking it provisional** — e.g. a `<!-- docket:example -->`
  line that `docket-lint` warns about until removed. Cheapest, and turns a silent
  wrong into a visible one, but leaves a foreign registry valid and usable
  indefinitely.

I lean toward generating a minimal registry, with `--link` continuing to link
`PROTOCOL.md` only. It is the option where the failure mode is loud, and the
`--link` rationale in the comment at lines 108-111 — that a linked store with no
registry "could not resolve a party name at all" — is satisfied by a generated
one just as well as by a shared one.

Routing to `agy` for the call rather than implementing, for the same reason as
r033: it changes what every downstream install gets, and `--link` semantics are
a design choice rather than a bug fix.

Done when: a fresh `docket-init` into an unrelated project, in both modes, leaves
that project with a registry that describes only itself, and editing it cannot
affect another project or the source clone; verified by the two-project
reproduction above.
