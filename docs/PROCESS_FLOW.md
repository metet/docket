# Docket MCP Process Flow & Architecture

This document visualizes the complete end-to-end architecture and runtime lifecycle of the **Docket MCP** protocol and tooling.

---

## 1. System Architecture & Component Interactions

```mermaid
flowchart TD
    %% SUBGRAPHS FOR SWIMLANES
    subgraph Agents["Participating AI Agents"]
        Agent["Agent Runtime / CLI<br/>(agy / claude / codex / qwen)"]
    end

    subgraph MCP["Docket MCP Server (tools/docket-mcp)"]
        RPC["stdio JSON-RPC 2.0 Router"]
        StoreRes{"Resolve Store & Workspace<br/>(local, trusted, roots)"}
        ToolList["Advertised Tools:<br/>• docket_list<br/>• docket_read<br/>• docket_open<br/>• docket_file<br/>• docket_close<br/>• docket_protocol"]
    end

    subgraph Core["Docket Core Layer"]
        Lib["docket_lib.py<br/>(Reducer, Validator, State Machine)"]
        New["tools/docket-new<br/>(Atomic Allocation & Authority Checks)"]
        Index["tools/docket-index<br/>(Derived INDEX.md Generation)"]
    end

    subgraph Storage["File-Based Store (Git Repository)"]
        Seq[".seq/ Lockdir<br/>Atomic Number Reservation"]
        Filings["docket/rNNN-*/<br/>• 000-request.md<br/>• 001-party-answer.md<br/>• NNN-party-disposition.md"]
        IdxFile["docket/INDEX.md<br/>(Whose Turn & Open Work)"]
    end

    subgraph Git["Git Boundary & Hooks"]
        CommitTool["tools/docket-commit --from <party>"]
        Hook{"tools/git-hooks/commit-msg<br/>Author matches staged filings?"}
        Remote[("Git Remote Repository<br/>(origin/main)")]
    end

    %% WORKFLOW CONNECTIONS
    Agent -->|"1. JSON-RPC Request (stdio)"| RPC
    RPC --> StoreRes
    StoreRes --> ToolList

    %% READ PATHS
    ToolList -->|"Read Tools (readOnlyHint=true)"| Lib
    Lib -->|"Read & Validate Filings"| Filings
    Lib -->|"Derive State (whose turn, status)"| IdxFile
    Lib -->|"Return JSON-RPC Text Content"| Agent

    %% WRITE PATHS
    ToolList -->|"Write Tools (open, file, close)"| New
    New -->|"Atomic mkdir (mutex)"| Seq
    New -->|"Append-only File Creation"| Filings
    New -->|"Regenerate Derived Index"| Index
    Index -->|"Write INDEX.md"| IdxFile
    New -->|"Return 'filed <path>'"| RPC

    %% COMMIT & PUSH
    Agent -->|"2. Stage Filings & Commit"| CommitTool
    CommitTool --> Hook
    Hook -- "Valid Party Match" --> Remote
    Hook -- "Mismatched Party" --> Reject["Refuse Commit<br/>(Block Attribution Leaks)"]

    %% STYLING
    classDef agentStyle fill:#e1f5fe,stroke:#0288d1,stroke-width:2px;
    classDef mcpStyle fill:#ede7f6,stroke:#512da8,stroke-width:2px;
    classDef coreStyle fill:#fff3e0,stroke:#f57c00,stroke-width:2px;
    classDef storeStyle fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef gitStyle fill:#fce4ec,stroke:#c2185b,stroke-width:2px;

    class Agent agentStyle;
    class RPC,StoreRes,ToolList mcpStyle;
    class Lib,New,Index coreStyle;
    class Seq,Filings,IdxFile storeStyle;
    class CommitTool,Hook,Remote,Reject gitStyle;
```

---

## 2. Multi-Agent Lifecycle & Turn Handoff

```mermaid
sequenceDiagram
    autonumber
    participant Requester as Requester (e.g. agy)
    participant MCP as Docket MCP Server
    participant New as docket-new
    participant Disk as Local Git Store
    participant Assignee as Assignee (e.g. claude / codex)
    participant Git as Git Remote

    %% OPENING A DOCKET
    Note over Requester,Disk: Step 1: Opening a Docket
    Requester->>MCP: docket_open(slug, title, body, assignee, workspace)
    MCP->>New: invoke kind=request, --from agy
    New->>Disk: atomic mkdir .seq/rNNN/
    New->>Disk: write 000-request.md (status: open, assignee: claude)
    New->>Disk: regenerate INDEX.md (waiting_on: claude)
    New-->>MCP: filed path
    MCP-->>Requester: filed docket/rNNN-slug/000-request.md
    Requester->>Git: docket-commit --from agy && git push

    %% ANSWERING & HANDOFF
    Note over Assignee,Disk: Step 2: Answering / Handoff
    Assignee->>MCP: docket_list (sees waiting_on: claude)
    Assignee->>MCP: docket_read(docket)
    Assignee->>MCP: docket_file(act: answer, body, assignee: codex)
    MCP->>New: invoke kind=filing, --from claude
    New->>Disk: write 001-claude-answer.md
    New->>Disk: regenerate INDEX.md (waiting_on: codex)
    Assignee->>Git: docket-commit --from claude && git push

    %% CLOSURE
    Note over Requester,Disk: Step 3: Resolution & Closure
    Requester->>MCP: docket_close(status: resolved, evidence: [...])
    MCP->>New: invoke kind=close, --from agy (verifies requester authority)
    New->>Disk: write 002-agy-disposition.md (status: resolved)
    New->>Disk: regenerate INDEX.md (closed: +1)
    Requester->>Git: docket-commit --from agy && git push
```

---

## 3. Key Design Principles

1. **Self-Asserted Identity Bound at Registration:**  
   `DOCKET_PARTY` is configured once per environment. The MCP server exposes no `from:` parameter, so an agent cannot forge another party's name.
2. **Strict Append-Only Immutability:**  
   No command or tool ever overwrites or deletes historical filings. Even corrections take the form of appended errata (`act: erratum`).
3. **Write-Time Authority Enforcement:**  
   Only the party who wrote `000-request.md` (the requester) is permitted to close a docket (`docket_close`). Any other party proposing closure must file `act: answer`.
4. **Autonomous Reduction & Pure Turn Routing:**  
   `waiting_on` is derived purely from file state by `docket_lib.reduce_docket`, avoiding lost turns across multiple agents.
5. **Git Boundary Checks:**  
   The `commit-msg` git hook ensures commit authorship matches the party who authored the staged filings, preventing accidental attribution cross-contamination.
