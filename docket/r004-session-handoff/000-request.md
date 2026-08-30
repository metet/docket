---
protocol: docket/0.2
id: r004/000
docket: r004
from: claude
to: [claude]
type: request
act: task
status: open
assignee: claude
refs: [PARTIES.md, BRD.md, tools/docket-mcp]
evidence: [git:fd08254, 36 checks 0 failing, 3 dockets closed r001 r002 r003]
date: 2026-08-30T12:00:09Z
---

# Open work carried across the session boundary

Carrying open work across a session boundary. Assigned to `claude` because a new
session starts with none of this and `docket_list` is the first thing it is told
to call.

**Why this is one docket and not eight.** `r003` decided one independently
decidable issue per docket, and this looks like a violation. It is not: the unit
of work here is the handoff, and its terminal state is a later session having
picked the threads up. The items below are pointers, not questions. Anything that
needs deciding becomes its own docket when someone acts on it — which is exactly
what `r003` prescribes.

## Open threads in this repo

**MCP conformance, in rough value order.** `initialize.instructions` — the
server can carry standing guidance at handshake instead of repeating it in every
tool description and in `AGENTS.md`, which matters most for the smallest-context
party. Then `resources` — dockets and filings are the textbook case for stable
URIs, and `resources/subscribe` would end polling, though note it does not wake an
idle party and never will. Then `prompts` (where `docket_protocol` belongs),
`outputSchema` for `docket_list`, and `completion/complete` for docket ids and
party names. The server still declares `2024-11-05`; annotations from `2025-03-26`
are already sent additively, and bumping the version needs an audit because that
revision added JSON-RPC batching, since removed, which the parse guard now rejects.

**`PARTIES.md` is incomplete.** Context budgets for `codex`, `agy` and `openclaw`
are `unverified`, and the file says not to guess one because under-estimating
wastes money and over-estimating silently truncates. `openclaw` is installed but
has never been onboarded and has no `mcp` subcommand in its build. `gemini` is
retired and could return through an API key rather than `oauth-personal`.

**BRD open questions.** Q1 hidden store, Q2 sub-dockets — partly answered by
`r003` rejecting them, worth recording there — Q3 one store per repo, which this
setup has already answered by accident: `flowboard` and this repo have separate
stores but share one `PARTIES.md` through a symlink, so parties are global and
dockets are per-repo. Q4 mandatory evidence on a disposition. Q5 archiving, which
was raised again and deferred again — the thing that grows is `INDEX.md`'s closed
section, which enters every party's context, not the directory listing, which
enters nobody's.

**Nothing runs `tools/docket-test`.** 36 checks and no hook or CI.

**A standing lint warning is expected**, not a defect: `r003/003` is an
ineffective erratum, kept as the record of a mistake.

## Open threads in the flowboard repo

`~/coding/qwen_code/mindmap`, scaffolded with a linked store and no dockets filed.
Two bugs found by review and never fixed: `input.js:14` calls `preventDefault` on
every Space keydown document-wide, which will block typing a space once in-shape
text editing exists, and `input.js:74-75` uses `e.clientX/Y` as SVG-local
coordinates, which drifts as soon as anything offsets the canvas. The BRD's NFR-5
still asks for Inter while NFR-1 forbids network calls; the agreed fix was to
amend NFR-5 to `system-ui` and it was never made. Eleven decisions from the
deleted chat log exist only in git history at `59a3cae`, in no docket and no spec.

## First move for whoever picks this up

Read this docket, then decide what is worth doing rather than doing it in order.
Close this one and open dockets for what you choose. Do not treat the list as a
queue: most of it has been deferred deliberately and at least twice.
