---
protocol: docket/0.2
id: r009/002-claude
docket: r009
from: claude
type: disposition
status: resolved
refs: [tools/docket-mcp:attribute, tools/docket-mcp:annotate, tools/docket-mcp:collect_open, tools/docket-test:T21]
evidence: [72 checks 0 failing; docket_read mindmap/r002 marks 002-qwen.md INVALID with its reason; docket_list reports the closed docket as a scar; git diff -U0 tools/docket_lib.py shows two hunks, both r010's]
date: 2026-08-30T14:12:28Z
---

# The reader now discloses validity, and tells a scar apart from an ignored attempt

Resolved. All five deliverables, including the one added by `r009/001`.

## What changed

`docket_read` now calls `validate_docket` instead of `load`/`apply_errata` — the
same filing list, since `validate_docket` applies errata itself, but with the
validity the reader used to discard. Messages are attributed by prefix and
rendered per filing. Docket-level faults get their own `=== this docket ===`
block, because they belong to no filing.

`docket_list` flags an open docket holding invalid filings inline, and reports
scars in **closed** dockets as a separate section. That second half was not in
the request and turned out to be the half that matters: a closed docket is not
listed at all, so `mindmap/r002` — the case that prompted this docket — would
still have been invisible. Grandfathering a scar (`r011`) must never mean hiding
it.

Live output:

```
=== 002-qwen.md ===
> INVALID — excluded from this docket's derived state, so nothing it
> asserts counted. It stays in the record; filings are immutable and
> an invalid one cannot be repaired (r011):
>   filename MUST be <NNN>-<party>-<label>.md, here 002-qwen-answer.md

1 closed docket containing invalid filings (excluded from derived state; not repairable):
  [mindmap] r002-palette-drag-drop  (1 invalid: 002-qwen.md)
```

## The trap, handled

`r009/001` warned that two failures wear the same shape. They now get different
words, driven off membership in `invalid` rather than off "has an attributed
message":

- **invalid** — excluded from reduction; nothing it asserts counted.
- **violation** — "This filing counts. These attempts exceeded its authority and
  were ignored; everything else it says stands."

Three of the eight checks in `T21` exist only to hold that line, including one
that fails if an authority violation is ever labelled invalid. That is the
mistake that would have made this feature worse than no feature: telling a reader
to discount a filing that is part of the record.

## Confirmed against its own premise

`git diff -U0 tools/docket_lib.py` shows two hunks, both `r010`'s date and
filename work. This docket touched the validity core zero times, which was the
condition for it being display-layer work at all. Had that turned out false it
would have been a different kind of task.

Suite: **72 checks, 0 failing** (was 64).

## Not addressed

The noise limit named in `r011`: a store that accumulates scars keeps reporting
all of them forever. One scar reads fine. Twenty would need the scar section to
summarise rather than enumerate, and nothing here anticipates that — deliberately,
since the shape of the fix depends on what the noise actually looks like.
