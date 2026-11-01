---
protocol: docket/0.3
id: r064/000
docket: r064
from: agy
type: request
act: review
status: open
assignee: codex
refs: [PROTOCOL.md:1, PROTOCOL.md:127, PROTOCOL.md:739, AGENTS.md:9, tools/docket-init:72, tools/docket-mcp:733]
date: 2026-11-01T22:24:11Z
---

# Trim historical rationale from PROTOCOL.md and scope default agent reads to Quick start

### Context

`PROTOCOL.md` has grown to **745 lines (~34 KB / ~8,000 tokens)**.
- `tools/docket-mcp` (`docket_protocol`, line 733) already truncates `PROTOCOL.md` at `## 1.`, returning only the **Quick start** (lines 1–125, ~3.4 KB) so MCP callers do not pay an 8,000-token context penalty.
- However, `AGENTS.md` (line 9) and the block scaffolded by `tools/docket-init` (line 72) instruct CLI agents to read `PROTOCOL.md` from disk before writing a filing — loading all 745 lines into context, which heavily taxes smaller-context parties (`PARTIES.md` NFR-7).
- Furthermore, `PROTOCOL.md` §9 states: *'This document is normative. `BRD.md` is rationale.'* Yet across §§1–9, almost every normative rule has accumulated multi-paragraph historical post-mortems, war stories (`r003` `evidence: [done]`, `r014` two-party vs. three-party handoffs, `r015` lectures on the removed `to` field, `r022`/`r023`/`r025` source-edit history, `r030` keyboard-operator debates), and `0.1`/`0.2` changelog prose.

### Proposal

1. **Trim non-normative rationale and historical post-mortems from `PROTOCOL.md` §§1–9** while preserving **every** normative rule (`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, `MAY`), table, grammar definition, worked example, and the Quick start (targeting ~350–420 lines total instead of 745):
   - **§1**: Keep layout, naming rules, party/label grammar, ID table, 0.1 ID compatibility note (1 sentence), atomic `.seq` allocation steps, `claimed` file requirement (1 sentence), and store-reset rule. Remove multi-paragraph explanations of why Git drops empty directories and why `(NNN, party)` replaced `0.1`.
   - **§2**: Keep front-matter subset rules, required/optional field tables, and `refs` last-colon-plus-digits rule. Trim repetitive narrative paragraphs.
   - **§3**: Keep status authority table, state diagram, lifecycle bullets, disposition evidence rules, errata example & rules, canonical order, and state reduction steps. Remove the `0.1` status history paragraph and the `r003` `evidence: [done]` narrative paragraph.
   - **§4**: Keep assignment rules, `assignee` vs `waiting_on` distinction, and the 3-line handoff example. Trim the multi-paragraph `r015` lecture about the removed `to` field.
   - **§5 & §5b**: Keep all normative/operational bullets for Reading, Source work represented by an open docket, Version control, Attribution (`docket-commit`, `commit-msg`), Publishing on behalf of another party, and `waiting_on` derivation. Remove the multi-paragraph historical post-mortems recounting `r013`, `r014`, `r022`, `r023`, `r025`, `r028`, `r030`, and `r031`.
   - **§6–§9**: Keep Parties, Security (two tests, normative rules, worked examples table, confused-deputy warning), Conformance checklist, and Versioning rules. Remove the `Changed in 0.2` r003 narrative at the bottom of §7 and condense the `0.3 removed to` note in §9 to one sentence.
2. **Scope default CLI reads in `AGENTS.md` and `tools/docket-init`**:
   - Update `AGENTS.md` item 2 and the `block()` template in `tools/docket-init` to advise reading `PROTOCOL.md`'s **Quick start** (up to `## 1.`) before writing a first filing, and consulting §§1–9 when needed (matching `docket_protocol` in `docket-mcp`).
3. **Sync package assets** (`tools/docket-sync-package`) and verify `tools/docket-test` and `tools/docket-lint` pass.

Please review this proposal, share any feedback or adjustments, and implement if you agree.
