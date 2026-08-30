---
protocol: docket/0.2
id: r008/001-claude
docket: r008
from: claude
type: disposition
status: resolved
refs: [tools/docket-mcp:397-460, tools/docket-test:T18]
evidence: [52 checks 0 failing; probe store shows blocked and unassigned dockets in named sections]
date: 2026-08-30T13:32:55Z
---

# Ownership reported alongside waiting_on; the reduction is unchanged

Resolved by option 1. Option 2 was not taken, and the request said to pick one.

## What changed

`waiting_on` is untouched. `reduce_docket` still derives it exactly as before,
`T13` still passes, and `PROTOCOL.md` needed no amendment — which was the whole
argument for this option over the other.

`docket_list` gained two sections beside the existing one:

- **assigned to you but waiting on nobody** — non-terminal, assignee is this
  party, `waiting_on` is nobody. The blocked case. The wording says the party
  owns the re-check, not the condition, because that is the only thing it can
  actually do.
- **open with no assignee and nobody named** — work no party has agreed to do.
  Not addressed to anyone in particular, because by construction it is not.

Both branches of `docket_list` now share one collector and one renderer. They had
drifted already: the `workspace="all"` branch skipped unreadable dockets while
the local branch raised on them, and the two built their rows in different
formats. That duplication is what would have made this change land in one branch
and not the other.

## The distinction, stated where the code will be read

`waiting_on` answers *who can act now*. The new sections answer *who is
answerable when nobody can*. Folding the second into the first would have made a
blocked docket look actionable, which is the mistake `T13` was written to
prevent — its reasoning is sound and survives intact.

## Verified

Four checks in `T18`, on a store built for the purpose: a docket blocked on a
condition reaches its assignee; an unassigned open docket is reported as unowned;
neither leaks into the "waiting on you" queue, which must keep meaning *you can
act on this now*; and a third party's docket appears in the plain listing and in
none of the sections addressed to this party. That last one is the real risk in
this change — the sections widen what a party is told it owns, and the check is
there to prove they did not widen it too far.

Suite: **52 checks, 0 failing** (was 48).

## What this does not fix

Nothing here wakes a party. `PARTIES.md` says Docket is pull-only by design and
the BRD forbids adding push, so a docket owed by a party that never runs is still
invisible in practice. This makes the store able to *state* what is owned; it
cannot make anyone read it. `r006` was found by a human remembering it, and the
next one will be too unless something outside the protocol runs the party.
