---
protocol: docket/0.2
id: r008/000
docket: r008
from: claude
to: [claude]
type: request
act: task
status: open
assignee: claude
refs: [tools/docket_lib.py:246-265, tools/docket-mcp:369-411, r006-mcp-initialize-instructions]
evidence: [probe: no-assignee open docket -> waiting_on=None; blocked-on-condition -> assignee=claude waiting_on=None; live: r006 status=blocked assignee=claude waiting_on=-]
date: 2026-08-30T13:18:16Z
---

# An open docket can be owed by nobody, and nothing reports that it is

## The defect

`reduce_docket` can derive `waiting_on = None` for a docket that is not
terminal. Two ways in, both reachable and both currently live:

**Blocked on an external condition.** `waiting_on` is `blocked_on` only when
`blocked_on` names a registered party; anything else routes to nobody. That is
deliberate and `T13` asserts it — no party can advance "upstream CI is red", and
naming one anyway invited someone to work on a blocked docket.

**No assignee, requester filed last.** The final branch reads
`st["assignee"] if last == st["requester"] else st["requester"]`. With no
assignee claimed, a requester who files twice is handed `None`.

Verified in a throwaway store:

```
no-assignee open docket -> status=open    assignee=None   waiting_on=None
blocked-on-condition    -> status=blocked assignee=claude waiting_on=None
```

## Why it matters

`docket_list` answers "what do I owe?" from the `waiting_on` section, and
`AGENTS.md` makes that section the first thing every party reads. A docket owed
by nobody is printed in the plain listing and named in no party's queue. It is
open, it is real work, and the mechanism built to surface open work steps over it.

**`r006` is the live instance**, opened in this same session:

```
[docket] r006-mcp-initialize-instructions  status=blocked  assignee=claude  waiting_on=-
```

It is assigned to `claude` and blocked on "a fresh client session". No party is
named, so no session will be told it exists. This is precisely the failure `r004`
was hand-rolled to work around — an entire docket written because open threads
had no way to reach the next session — and the protocol reproduces it whenever a
docket is blocked on anything but a party.

## The distinction the model is missing

Two different facts are being collapsed into one field:

- **who can advance this now** — correctly nobody, for an external condition;
- **who owns it** — the assignee, who still owes the re-check, and owes deciding
  whether the condition has changed or the docket should be withdrawn.

`waiting_on` answers the first. Nothing answers the second, so ownership
evaporates the moment work is blocked.

## What to do

Decide between these; do not do both.

1. **Report it rather than re-deriving it.** Leave `waiting_on` exactly as it is —
   the reasoning behind `T13` is sound — and give `docket_list` a second section:
   *blocked, assigned to you*, listing non-terminal dockets whose `assignee` is
   this party and whose `waiting_on` is nobody. Cheapest, changes no derived
   state, breaks no existing check.
2. **Distinguish the fields.** Add a derived `owner`, separate from `waiting_on`,
   and have every consumer say which it means. More honest, more surface, and it
   touches `PROTOCOL.md` §3, which makes it a spec change rather than a tooling
   one.

Either way, an open docket assigned to nobody at all — the second cause above —
should be surfaced somewhere as unowned. That one is not a routing subtlety; it
is work that no party has agreed to do.

## Terminal state

`r006` reaches a session that did not open it, without a human remembering it
exists.
