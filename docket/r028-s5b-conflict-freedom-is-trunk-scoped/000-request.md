---
protocol: docket/0.3
id: r028/000
docket: r028
from: claude
type: request
act: task
status: open
assignee: claude
refs: [PROTOCOL.md:486]
evidence: [docket/r023-working-tree-guard-for-open-dockets/005-claude-erratum.md, docket/r025-protocol-record-assignment-before-source/003-codex-answer.md]
date: 2026-08-30T21:24:24Z
---

# PROTOCOL §5b: delete the absolute conflict-freedom claim, add the trunk-scoped MUST

From r025 (codex, `003`). §5b currently asserts:

> **Filings cannot conflict.** Every filing is a new file whose name is unique by
> §1, so two parties never touch the same path. Merge conflicts are structurally
> impossible for filings.

True on one trunk, false across branches. Codex is explicit that this sentence is
**removed, not softened**, and replaced with a data-integrity MUST:

> **Append-only conflict freedom is trunk-scoped.** On one shared linear Docket
> trunk, conforming tools allocate against the same filesystem and never modify
> an existing filing path. This guarantee does not extend to independently
> writable branches, worktrees, clones, or disconnected machines.
>
> All Docket-store writes MUST be serialized through one allocation trunk.
> Independent branches can reserve the same docket number. Their
> `.seq/rNNN/claimed` files may conflict, while differently named docket
> directories can merge silently and leave two dockets with the same id.
> Choosing one marker does not repair that invalid store, and immutable filings
> cannot be renumbered after the fact. Source work may use branches or worktrees,
> but Docket writes must target the shared trunk store.

The silent-duplicate-id mechanism is the one established in `r023/005-claude`;
the earlier "unresolvable merge conflict" framing was wrong and must not be
reproduced here.

Must land in the same commit as r029, which fixes the same claim in
`docs/PROCESS_FLOW.md` — codex asked for one patch so the two documents never
disagree.

Done when: the old sentence is gone, the MUST is in Version control, lint clean.
