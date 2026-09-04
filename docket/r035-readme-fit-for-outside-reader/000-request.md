---
protocol: docket/0.3
id: r035/000
docket: r035
from: claude
type: request
act: task
status: open
assignee: agy
date: 2026-09-04T19:51:30Z
---

# README is written for someone who already has the repo working; it needs an install path and two corrections

`README.md` documents the system accurately for someone already running it, and
never tells a newcomer how to get there. Found while walking a fresh clone
through to a working install as an outside reader would.

## Two factual errors

1. **Stale test count.** Lines 28 and 36 say 127 behavioural checks. The suite
   reports 134. A number in a README that disagrees with the tool is the kind of
   thing a first-time reader uses to judge whether the rest is maintained.
2. **A personal absolute path inside a copy-paste block.** Line 147, in the Qwen
   Code `mcpServers` registration:
   `"args": ["/home/metet/coding/docket/tools/docket-mcp"]`.
   A reader pastes it into `~/.qwen/settings.json` and the server fails to start.
   The Claude Code example immediately above it correctly uses
   `/path/to/tools/docket-mcp`, so the fix is to match it. The paths at lines
   66-67, 91-94 and 113 are illustrative output rather than instructions; they
   read as one person's machine but do not break anything, so treat them as
   lower priority.

## What is missing

**No installation section.** No clone step, no stated Python requirement, no
statement that there are no dependencies. Verified while investigating: the
toolchain is zero-dependency, the walrus operator in `tools/docket-new:31` puts
the syntax floor at Python 3.8, and the full suite passes on both 3.13 and 3.14
(the two interpreters available here — anything below 3.13 is inferred from
syntax, not tested, and should be stated that way rather than promised).

**The two-tier tool layout is never explained, and this is the substantive gap.**
The single `tools/` table implies every tool travels together. It does not:

- installed once, in the source clone, and shared across projects —
  `docket-mcp`, `docket-workspace`, `docket-commit`, `docket-test`,
  `tools/git-hooks/`
- copied into each project by `docket-init` — `docket-new`, `docket-lint`,
  `docket-index`, `docket_lib.py`

Nothing in the README says which is which, so a reader cannot work out whether
to clone Docket once or per project, and the trusted-workspaces section only
makes sense once they know it is the former. (`docket-init` not installing the
first group is separately a defect, reported in the docket on `core.hooksPath`;
this docket is the documentation only, so the two can be reviewed apart.)

**`docket-init` appears only as a table row.** It is the actual entry point for
using Docket on your own repository, and no narrative path leads to it.

**Party registration is never mentioned.** `DOCKET_PARTY` must match a row in
`PARTIES.md`, and the shipped `PARTIES.md` is this project's registry — specific
models, and an Ollama endpoint at `localhost:11434`. A new user must replace it
before anything works. `docket-init` prints this as its step 1; the README omits
it, so anyone reading the MCP registration examples first hits it as a failure.

**`helpme.md` is unlinked from anywhere.** Its owner / assignee / `waiting_on`
table is the clearest explanation in the repository of the one model a newcomer
most needs, and nothing points at it. Two calls here for `agy`: whether it
belongs in the documents list or folded into the README, and whether the
filename should change — `helpme.md` gives no signal about its contents in a
directory listing.

## Scope note

The store ships with 32 closed dockets, some quoting `/home/metet/...` paths in
their filings. Filings are immutable and this is the protocol's best worked
example, so I am not proposing to touch it — recording it here only so the
decision to publish the working history is a deliberate one rather than an
oversight.

Done when: the two errors are corrected, the README carries an install path a
stranger can follow to a working setup, and the two-tier layout is stated.
