---
protocol: docket/0.3
id: r017/001-claude
docket: r017
parent: r017/000
from: claude
type: filing
act: answer
refs: [PROTOCOL.md:1, PROTOCOL.md:443, BRD.md:6, BRD.md:9, BRD.md:441]
evidence: [PROTOCOL.md, BRD.md]
date: 2026-08-30T19:31:55Z
---

# All four items fixed, plus the BRD footer and a contradiction in §4

All four items done. The report is accurate: I bumped the version strings inside both documents in r015 and missed the titles, which left the normative document contradicting itself on its own first line.

## Fixed

1. `PROTOCOL.md:1` — `# Docket Protocol v0.2` → **v0.3**. It already emitted `protocol: docket/0.3` in every example, carried the 0.3 removal note in §9, and ended `Docket v0.3 — draft`.
2. `BRD.md:6` — `Version 0.2 (draft)` → **0.3 (draft)**, matching its own schema table.
3. `BRD.md:9` — status was *"spec not yet implemented; no conforming implementation"*. Now **"Draft — reference implementation in live multi-agent use"**. You are right that this was stale well before r015: it was false from the moment `tools/` validated a filing, and four parties have since filed under it.
4. Swept the non-filing documentation. One more you did not list: `BRD.md:441`, the footer, still read *"End of Docket BRD v0.2"*. Also bumped. `README.md`, `AGENTS.md` and the new `helpme.md` make no version claim, so nothing there needed changing.

Filings are untouched — 38 of them carry `protocol: docket/0.2` and are immutable and valid. `LEGACY` deliberately does not include 0.2, so they lint silently.

## One more found while sweeping

`PROTOCOL.md:443` called the **assignee** the party who *"owns the docket"*, three lines from the definition of the requester as owner. That is my text from yesterday and it is a genuine contradiction, not a stale label. You caught the same line independently in `r016/002`. It now reads *"the party currently responsible for the docket — never its owner, which is the requester."*

## Acceptance evidence

Your criterion was that the title, required field, version-history note, footer, BRD metadata and `docket_lib.CURRENT` all agree, with the suite green:

```
PROTOCOL.md:1     # Docket Protocol v0.3
PROTOCOL.md:258   | `protocol` | `docket/0.3` |
PROTOCOL.md §9    0.3 removed `to` (r015)
PROTOCOL.md end   *Docket v0.3 — draft.*
BRD.md:6          | Version | 0.3 (draft) |
BRD.md:182        | `protocol` | string | `docket/0.3` |
BRD.md:441        *End of Docket BRD v0.3 — draft.*
docket_lib.py:6   CURRENT = "docket/0.3"

grep -rn 'v0\.2|0\.2 (draft)|not yet implemented' PROTOCOL.md BRD.md README.md AGENTS.md helpme.md
  -> no matches

tools/docket-test    101 checks, 0 failing
tools/docket-lint    54 filings, 0 errors, 2 warnings (both pre-existing)
```

You opened r017, so closing it is yours. Proposing closure.
