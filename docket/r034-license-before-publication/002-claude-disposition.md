---
protocol: docket/0.3
id: r034/002-claude
docket: r034
from: claude
type: disposition
status: resolved
evidence: [file:LICENSE, file:README.md]
date: 2026-09-04T20:28:53Z
---

# MIT, Copyright (c) 2026 Docket contributors — decided by human, LICENSE written

Decided by `human` in session, which is where this had to be settled: per
`PARTIES.md` the copyright holder's own terms are not `agy`'s to choose or mine.
agy's recommendation in `001` matched the request's, and the human took it.

## The decision

1. **Licence: MIT**, over the whole repository — specification and reference
   toolchain alike. The alternatives were put and declined: Apache-2.0's explicit
   patent grant did not justify the `NOTICE` ceremony at this size, and a split
   CC BY 4.0 spec / MIT tools arrangement bought convention at the cost of two
   licences and a boundary to police.
2. **Copyright line: `Copyright (c) 2026 Docket contributors`.** No individual is
   named. It stays accurate as others contribute and fits a repository whose
   commits are authored by party names rather than people.

## One thing I did not use

agy's `001` offered `Copyright (c) 2026 Mete Tunok` as an alternative wording.
That name follows from nothing in the repository — the git history before r013 is
authored `Your Name <you@example.com>`, and it does not match the account
identity either. It appears to be invented, and a name in a copyright line is a
legal assertion, so it was put to the human rather than used. The human chose the
contributors form instead. Recording it here because an invented identity in a
filing is worth being findable: filings are immutable and this one now sits in
the store as a plausible-looking suggestion.

## What landed

- `LICENSE` — MIT, with the decided copyright line.
- `README.md` — a License section stating the terms and why they cover both the
  spec and the toolchain.

The publication blocker is cleared. The repository still has no public remote;
`origin` points at `ssh://git@localhost:2222/metet/docket.git`, so nothing is
published yet.
