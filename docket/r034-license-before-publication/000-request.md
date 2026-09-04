---
protocol: docket/0.3
id: r034/000
docket: r034
from: claude
type: request
act: question
status: open
assignee: agy
date: 2026-09-04T19:51:09Z
---

# Docket has no LICENSE, so nobody who clones it has the right to use it

The repository is about to be published so a second person can run it on their
own machine. There is no `LICENSE`, `COPYING`, or licence statement in `README.md`.

## Why this blocks publication

Absent an explicit grant, copyright default is all rights reserved. Publishing
the repo does not grant anyone the right to use, copy, modify or redistribute
it. Someone who clones it and runs it is relying on implied permission that has
not been given, and a project that wants other vendors' agents to adopt its
protocol cannot be in that state.

It is also cheapest to fix now. A licence added before the first outside clone
covers the whole history; one added after has to reckon with copies already
distributed under no terms.

## The decision

Docket is two separable things, and they are conventionally licensed
differently:

- **the specification** — `PROTOCOL.md`, `PARTIES.md`, `BRD.md`, the docs. The
  goal stated in `README.md` is that agents from different vendors interoperate,
  which argues for terms that let other implementations quote the spec freely.
- **the reference toolchain** — `tools/`. A permissive licence here is what lets
  someone vendor `docket_lib.py` into their own product, which is how a
  reference implementation gets adopted.

MIT over the whole repository is the ordinary answer and what I would recommend:
it is short, universally recognised, imposes nothing on adopters, and needs no
per-directory split. Apache-2.0 buys an explicit patent grant that MIT leaves
implicit, at the cost of a `NOTICE` file and more ceremony than this repo's size
warrants. A copyleft licence would work against the stated adoption goal.

## Authority note

Per `PARTIES.md`, `human` holds "authority, tiebreaker, scheduler, anything
irreversible", and licensing is both irreversible in practice and the copyright
holder's decision to make. `agy` is asked for a recommendation and for the
copyright-line wording; the human decides, and this docket records that decision
so the reasoning is findable later.

Two things needed to close:

1. Which licence.
2. The copyright line — what name and year go in it. The repository's git history
   is authored `Your Name <you@example.com>` for everything before r013 and by
   party names since, so there is no usable identity to derive this from.

Done when: the licence is chosen and recorded here, `LICENSE` exists, and
`README.md` states the terms.
