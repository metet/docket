# Docket MCP Process Flow & Architecture

This document visualizes the end-to-end architecture and runtime lifecycle of the
**Docket** protocol and tooling.

Corrections in this revision were established by review in `r024`; the reasoning
behind the non-obvious ones is kept inline so a later editor does not undo them.

---

## 1. System Architecture & Component Interactions

```mermaid
flowchart TD
    subgraph Agents["Participating AI Agents"]
        Agent["Agent runtime<br/>agy · claude · codex · qwen"]
        Shell["Direct CLI use<br/>tools/docket-new, tools/docket-index"]
    end

    subgraph MCP["Docket MCP Server — tools/docket-mcp"]
        RPC["stdio JSON-RPC 2.0 router"]
        StoreRes{"Resolve store<br/>1. DOCKET_STORE absolute or found from cwd<br/>2. trusted workspace containing cwd<br/>3. client roots capability<br/>success is cached; a failure is retried"}
        Find["find_docket_store<br/>cross-workspace lookup by id or slug<br/>backs the workspace parameter"]
        ToolList["Advertised tools<br/>read: docket_list · docket_read · docket_protocol<br/>write: docket_open · docket_file · docket_close"]
        Collect["collect_open<br/>derives whose turn it is, in memory, per call"]
    end

    subgraph Core["Docket Core Layer"]
        Lib["docket_lib.py<br/>reducer · validator · errata model"]
        New["tools/docket-new<br/>atomic .seq reservation · authority checks<br/>does NOT regenerate the index"]
        Index["tools/docket-index<br/>the only writer of INDEX.md"]
        Lint["tools/docket-lint<br/>validates the store · --gate for one commit"]
        Ws["tools/docket-workspace<br/>trusted workspace registry"]
    end

    subgraph Storage["File-Based Store (Git Repository)"]
        Seq[".seq/rNNN<br/>atomic number reservation"]
        Filings["docket/rNNN-slug/<br/>000-request.md<br/>NNN-party-answer.md<br/>NNN-party-disposition.md"]
        IdxFile["docket/INDEX.md<br/>derived artefact for humans and session startup<br/>never an input to any read tool"]
    end

    subgraph Git["Git Boundary & Hooks"]
        CommitTool["tools/docket-commit --from party<br/>author per invocation · Docket-Party trailer"]
        Pre{"pre-commit<br/>docket-lint, plus docket-test in this repo<br/>checks the WORKING TREE, not the index"}
        Hook{"commit-msg<br/>declared party vs parties in staged filings"}
        Remote[("origin/main")]
    end

    %% READ PATH
    Agent -->|"JSON-RPC over stdio"| RPC
    RPC --> StoreRes
    StoreRes --> ToolList
    StoreRes -.->|"id names another workspace"| Find
    Find --> Filings
    ToolList -->|"docket_list"| Collect
    ToolList -->|"docket_read"| Lib
    Collect --> Filings
    Lib -->|"read · validate · apply errata"| Filings
    Lib -->|"text content"| Agent

    %% WRITE PATH
    ToolList -->|"docket_open · docket_file · docket_close"| New
    New -->|"exclusive mkdir — the reservation itself"| Seq
    New -->|"append-only, never overwrite"| Filings
    New -->|"path on stdout"| RPC
    RPC -->|"regenerate after docket-new exits 0<br/>failure warns; the filing still stands"| Index
    Index --> Lib
    Index -->|"the only write of INDEX.md"| IdxFile

    %% CLI PATH — the asymmetry worth knowing
    Shell -->|"filing straight from the shell"| New
    Shell -.->|"MUST be run by hand;<br/>nothing else will"| Index

    %% GIT BOUNDARY
    Agent -->|"stage and commit"| CommitTool
    CommitTool --> Pre
    Pre -- "lint or suite fails" --> RejectA["Refuse commit"]
    Pre -- "clean" --> Hook
    Hook -- "party agrees with staged filings" --> Remote
    Hook -- "party contradicts them" --> RejectB["Refuse commit<br/>wrong attribution is worse than none"]
    Hook -- "no party declared" --> WarnC["Warn, allow<br/>the human owns the repo"]
    WarnC --> Remote
    Ws -.->|"registers paths consulted by"| StoreRes
    Lint --> Lib

    classDef agentStyle fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef mcpStyle fill:#ede7f6,stroke:#512da8,stroke-width:2px;
    classDef coreStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef storeStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef gitStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px;

    class Agent,Shell agentStyle;
    class RPC,StoreRes,ToolList,Collect,Find mcpStyle;
    class Lib,New,Index,Lint,Ws coreStyle;
    class Seq,Filings,IdxFile storeStyle;
    class CommitTool,Pre,Hook,Remote,RejectA,RejectB,WarnC gitStyle;
```

### Two things the diagram is drawn to make unmissable

**`docket-new` never regenerates the index.** The only caller of `docket-index`
is `docket-mcp`, in `run_new`, after `docket-new` has exited 0. So a filing made
**through the CLI leaves `INDEX.md` stale** until someone runs
`python3 tools/docket-index <store>` by hand. If the reindex fails, the MCP write
still reports success and appends a warning naming the repair — the filing is
already on disk and immutable, and reporting the whole call as failed would
invite a retry that writes a duplicate nobody can delete.

**The read path never touches `INDEX.md`.** `docket_list` derives state live
through `collect_open`, and `docket_read` goes through `docket_lib`. Neither
reads the index. A stale `INDEX.md` misleads humans and session startup; it
cannot corrupt a tool result.

---

## 2. Multi-Agent Lifecycle & Turn Handoff

Two shapes matter. The first is the ordinary one — the assignee answers and the
**requester** owes the next move. The second is a handoff, where the assignee
names a different party.

```mermaid
sequenceDiagram
    autonumber
    participant Req as Requester (agy)
    participant MCP as Docket MCP Server
    participant New as docket-new
    participant Idx as docket-index
    participant Disk as Local Git Store
    participant Asg as Assignee (claude)
    participant Git as Git Remote

    Note over Req,Disk: Step 1 — Opening a docket
    Req->>MCP: docket_open(slug, title, body, assignee: claude, workspace?)
    MCP->>New: kind=request, --from agy
    New->>Disk: atomic mkdir .seq/rNNN
    New->>Disk: write 000-request.md (status: open, assignee: claude)
    New-->>MCP: path on stdout
    MCP->>Idx: regenerate
    Idx->>Disk: write INDEX.md (waiting_on: claude)
    MCP-->>Req: filed docket/rNNN-slug/000-request.md
    Req->>Git: docket-commit --from agy && git push

    Note over Asg,Disk: Step 2 — The ordinary answer, with no reassignment
    Asg->>MCP: docket_list (waiting_on: claude)
    Asg->>MCP: docket_read(rNNN)
    Asg->>MCP: docket_file(act: answer, body)
    MCP->>New: kind=filing, --from claude
    New->>Disk: write 001-claude-answer.md
    MCP->>Idx: regenerate
    Note right of Idx: assignee is unchanged, so the reducer routes<br/>waiting_on back to the REQUESTER, who now owes<br/>a close, an objection or a follow-up.<br/>This is correct behaviour, not a stale field.
    Idx->>Disk: write INDEX.md (waiting_on: agy)
    Asg->>Git: docket-commit --from claude && git push

    Note over Asg,Disk: Step 2b — Handoff, only when a third party should act
    Asg->>MCP: docket_file(act: answer, body, assignee: codex)
    Note right of Asg: only the requester or the current assignee<br/>may reassign; anyone else is refused
    MCP->>Idx: regenerate
    Idx->>Disk: write INDEX.md (waiting_on: codex)

    Note over Req,Disk: Step 3 — Resolution and closure
    Req->>MCP: docket_close(status: resolved, evidence: [...])
    MCP->>New: kind=close, --from agy — requester authority verified
    New->>Disk: write 00N-agy-disposition.md (status: resolved)
    MCP->>Idx: regenerate
    Idx->>Disk: write INDEX.md (closed +1)
    Req->>Git: docket-commit --from agy && git push
```

---

## 3. Correcting a Filing — Errata

Filings are immutable, so a mistake is corrected by **appending**, never by
editing. This is the one flow whose rules are not guessable from the tool names.

```mermaid
flowchart LR
    Wrong["001-claude-answer.md<br/>a field is wrong"]
    Err["002-claude-erratum.md<br/>act: erratum<br/>supersedes: rNNN/001-claude<br/>corrects: refs, evidence"]
    Check{"Is the field correctable?<br/>refs · evidence · blocked_on · parent · date"}
    Applied["Reader sees the corrected value.<br/>docket_read marks the target<br/>'corrected by a later erratum'"]
    Ignored["Accepted, warned about, IGNORED<br/>e.g. an erratum against act"]

    Wrong --> Err
    Err --> Check
    Check -- "yes" --> Applied
    Check -- "no" --> Ignored

    classDef ok fill:#e8f5e9,stroke:#388e3c;
    classDef no fill:#fce4ec,stroke:#c2185b;
    class Applied ok;
    class Ignored no;
```

A party may only correct **its own** filings. The original is never touched: both
filings stay on disk, and the correction is applied at read time by the reducer.

---

## 4. Key Design Principles

1. **Identity is an ergonomic guard, not authentication.**
   `DOCKET_PARTY` is bound at registration and no MCP tool takes a `from`
   argument, so an agent working through MCP has no forging affordance. That is
   the whole of the guarantee. The CLI takes `--from <party>` for any party in
   `PARTIES.md`, every party shares one clone, one OS user and one key, and every
   name written inside a filing is self-asserted (PROTOCOL §7). Nothing here
   authenticates anyone, and no document should suggest otherwise.

2. **Strict append-only immutability.**
   No tool overwrites or deletes a filing. Corrections are appended as errata
   (§3). This is also why a guess is dangerous — a docket opened in the wrong
   store cannot be withdrawn by anyone but its requester.

3. **Write-time authority enforcement.**
   Only the requester — the party named in `000-request.md`, which is derived and
   never written as a field — may close a docket. Any other party proposing
   closure files `act: answer`. Reassignment and `status: blocked` are gated to
   the requester or the current assignee.

4. **Turn routing is derived, never authored.**
   `waiting_on` is computed by `docket_lib.reduce_docket` from the filings alone;
   no party writes it. `assignee` is authored and persistent; `requester` is
   derived and immutable. There is deliberately no `implementer` field — a
   reducer cannot infer an implementer nobody wrote down, so such a field would
   carry the same hand-maintained fact with the same omission risk (`r022`).

5. **Two git hooks, with different jobs.**
   `pre-commit` runs `docket-lint` — `--gate`d to the filings in the commit — and
   the full `docket-test` suite when this is the toolchain's own repository. It
   inspects the **working tree, not the staged content**, so a partial `git add`
   can commit a state it never saw. `commit-msg` then compares the declared party
   (the `Docket-Party:` trailer, falling back to the author name only when that
   looks like a party name) against the parties named in staged filings, and has
   three outcomes: agreement passes, contradiction is **blocked**, and a commit
   declaring no party at all is **warned about and allowed** — the human
   committing tooling does not answer to this hook.

6. **The store is a single linear trunk.**
   `.seq` mutual exclusion is an atomic `mkdir`, and it is only mutual exclusion
   on **one shared filesystem**. Parties on separate branches or worktrees each
   allocate against their own copy and reach the same next number.

   The damage is not the conflict you would expect. `.seq/rNNN/claimed` does
   conflict, but it is a marker rather than a filing — §1 does not apply and
   resolving it is harmless. The docket directories are at *different paths*, so
   git merges both **silently**, leaving two dockets sharing one id that cannot
   be renumbered without renaming filings. A conflict would at least halt the
   merge; this does not.

   PROTOCOL.md §5b states the normative rule: all Docket-store writes MUST be
   serialized through one allocation trunk. Source may branch; `docket/` may not
   (`r023`, `r028`).
