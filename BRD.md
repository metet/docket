# Business Requirements Document (BRD) — Docket

| Field        | Detail                                                        |
| ------------ | ------------------------------------------------------------- |
| Project Name | **Docket**                                                     |
| Version      | 0.3 (draft)                                                    |
| Date         | 2026-08-29                                                     |
| Author       | metet (personal project — self-funded)                         |
| Status       | Draft — reference implementation in live multi-agent use       |

> **Docket** is a file-based protocol that lets AI coding agents from different
> vendors collaborate on the same repository, using nothing but the filesystem.

---

## 1. Business Context & Objective

### 1.1 Problem

Agent CLIs from different vendors cannot talk to each other. Each ships its own
context format, tool schema, permission model, and increasingly its own agent
protocol. The practical consequences:

- **Collaboration requires a shared runtime.** Existing multi-agent frameworks
  (group chat, supervisor graphs, role crews) assume all participants live in one
  process with one orchestrator. Independent CLIs do not.
- **Vendor protocols pull toward lock-in.** Adopting one vendor's agent-to-agent
  mechanism makes the *other* vendors' agents second-class participants.
- **The obvious fallback — a shared chat log — does not scale.** A single appended
  transcript grows without bound, has no notion of whose turn it is, none of what
  is still open, and no way to stop. Every participant re-reads the entire history to
  contribute one message.

The last point is not hypothetical. This protocol's motivating incident: a single
`chatroom.md` file in which one agent asked eleven questions and another answered
all eleven in one reply. Nothing in the file could express which questions were
settled, which were disputed, or which remained open.

### 1.2 Objective

Define a **transport-free, vendor-neutral protocol** for asynchronous
collaboration between heterogeneous AI agents, in which:

- the unit of communication is a **request** with a lifecycle and a terminal state,
- records are **immutable and append-only**, so concurrent writers cannot clobber,
- participation requires **only file read/write** — no SDK, no daemon, no network,
- the whole exchange remains **human-readable and greppable** at rest.

### 1.3 Success Metrics

| Metric | Target |
| ------ | ------ |
| Time for a new agent to emit its first valid filing, given only `PROTOCOL.md` | < 1 turn, no correction |
| Filings that are schema-valid without human correction | > 95% per party, **including the weakest participant** |
| Dockets reaching a terminal state (vs. silently abandoned) | > 90% — measures the operating loop, not the protocol: pull-only means closure depends on the scheduler running requesters, so `waiting_on` exists to make that actionable |
| Context required to participate in one docket | One docket subtree — never the full history |
| Vendors interoperating on one docket | ≥ 3 |

---

## 2. Participants

Docket assumes **capability-asymmetric** participants. This is a design input, not
an edge case: the cheap local model and the frontier model are both first-class,
and the protocol must be emittable by the weaker one.

| Party | Runtime | Context budget | Typical role |
| ----- | ------- | -------------- | ------------ |
| Local quantised model | e.g. Qwen Code → llama.cpp/Ollama | Small | Implementation, bulk work, ~zero marginal cost |
| Frontier model | e.g. Claude Code, Codex, Gemini CLI | Large | Review, root-cause analysis, spec work |
| Human | Terminal | — | Scheduler, tiebreaker, authority |

**The human is a participant, not an operator.** Docket does not assume an
automated supervisor exists. If one is added later it is simply another party.

---

## 3. Scope

### 3.1 In Scope

| #  | Capability | Priority |
| -- | ---------- | -------- |
| S1 | Request-scoped conversation: one parent request, many immutable child filings | Must |
| S2 | A lifecycle with explicit terminal states, and rules for who may close | Must |
| S3 | A record schema carrying identity, threading, and evidence | Must |
| S4 | Assignment and derived turn-taking across ≥ 2 parties | Must |
| S5 | A derived index of open work — generated, never hand-maintained | Must |
| S6 | A participant registry (`PARTIES.md`) declaring each party's capabilities and cost | Should |
| S7 | Per-tool onboarding convention (`CLAUDE.md` / `QWEN.md` / `GEMINI.md` / `AGENTS.md`) | Should |
| S8 | A reference implementation of the index generator and a new-filing helper | Should |

### 3.2 Non-Goals

A protocol is defined as much by refusal as by capability.

- **Not a tool-calling or RPC mechanism.** That is MCP's job. Docket carries
  *correspondence*, not function invocations.
- **No push, no notification, no wake-up.** Docket is pull-only. Something outside
  the protocol — a human or a supervisor — decides when an agent runs, and the
  protocol MUST NOT be extended to assume otherwise. The cost is real: a docket
  answered by its assignee stays open until its requester is run again. Mitigated
  by deriving `waiting_on` (FR-6), not by adding push.
- **No orchestration or scheduling.** Turn order, budgets, and loop detection belong
  to a supervisor built *on* Docket, not inside it.
- **No authentication or cryptographic identity in v0.1.** See §7.
- **No real-time or streaming semantics.** Turn latency is human- or
  supervisor-paced, measured in minutes.
- **Not a replacement for version control.** Docket rides on git and inherits its
  history, attribution, and diffing rather than reimplementing them.
- **No inline binary payloads.** Artifacts are referenced by path, not embedded.
- **Not a knowledge base.** Dockets record decisions and their justification; they
  are not where documentation lives.

---

## 4. Conformance Language

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are
to be interpreted as described in RFC 2119.

An implementation is **conforming** if it satisfies every MUST in §5 and passes the
acceptance criteria in §9.

---

## 5. Functional Requirements

### FR-1 Storage Layout

A Docket store is a directory, by convention `docket/`, at the root of the
repository the parties are collaborating on.

```
docket/
  PROTOCOL.md          present, OR referenced by relative path from README.md
  PARTIES.md           participant registry (§FR-7)
  INDEX.md             GENERATED — never hand-edited (§FR-6)
  r001-grid-coverage/
    000-request.md
    001-claude-answer.md
    002-qwen-objection.md
    003-claude-disposition.md
  r002-palette-layout/
    000-request.md
```

- Each docket MUST be a directory named `r<NNN>-<slug>`.
- Docket numbers MUST be allocated atomically, by exclusive creation of a
  reservation directory `.seq/r<NNN>`, retrying on collision. Reservations are
  never deleted, so a number is never reused. "Highest + 1" is a race.
- A filing's identity is its path: `<docket>/000` for the request, otherwise
  `<docket>/<NNN>-<party>`. Because `(NNN, party)` is unique within a docket, two
  parties choosing the same sequence number produce distinct ids, so `parent` and
  `evidence` are never ambiguous.
- The request MUST be named `000-request.md`; it cannot collide, since creating
  the docket directory and creating `000` are one act.
- Every other filing MUST be named `<NNN>-<party>-<label>.md`. The party segment
  is required — it is what makes a duplicate sequence number survivable. The
  label is free-form and is deliberately **not** tied to the `act` enum.
- Filings MUST NOT be modified or deleted after creation. Correction is expressed
  by appending a new filing, never by editing an old one.
- Sequence numbers SHOULD be monotonic within a docket. Two parties writing the
  same number concurrently is a tolerated collision, not an error: the party name
  is in the filename, and the id carries it too, so the two filings are distinct
  rather than merely both present. Ordering is by `(sequence, party)`, never by
  `date` — see FR-6.

*Note: this last rule trades strict ordering for lock-free concurrency. It is the
right trade while turns are human-paced. A server-mediated implementation (§10)
can assign sequence numbers authoritatively and remove the ambiguity.*

### FR-2 Record Format

Every filing MUST be a Markdown file beginning with a YAML front-matter block,
followed by a free-form Markdown body.

**Required fields** — every filing:

| Field | Type | Meaning |
| ----- | ---- | ------- |
| `protocol` | string | `docket/0.3` — the spec version this filing claims |
| `id` | string | `<docket>/000` for a request, else `<docket>/<NNN>-<party>` — e.g. `r003/002-qwen`. Globally unique within the store |
| `docket` | string | `r003` — the parent request |
| `from` | string | Party name, as registered in `PARTIES.md` |
| `type` | enum | `request` \| `filing` \| `disposition` (structural role) |
| `date` | RFC 3339 | Creation timestamp, UTC |

**Optional fields:**

| Field | Type | Meaning |
| ----- | ---- | ------- |
| `parent` | string | Filing this responds to. Absent means the request |
| `act` | enum | `question` \| `task` \| `review` \| `report` \| `answer` \| `objection` \| `ack` |
| `assignee` | string | Party responsible for advancing the docket |
| `status` | enum | `open` \| `blocked` \| `resolved` \| `withdrawn` — MAY appear on any filing, but only with authority (FR-3): `resolved`/`withdrawn` are the requester's alone via `type: disposition`; `blocked`/`open` may be set by the requester or current assignee. A status set without authority is ignored in reduction and reported by lint |
| `refs` | list | Source locations, as `path:line` |
| `evidence` | list | Proof: `git:<sha>`, a file path, or command output |
| `blocked_on` | string | Party or external condition being waited on |

The `type`/`act` split separates a filing's structural role from its speech act,
following FIPA-ACL's performatives. `type` drives the state machine; `act` conveys
intent.

**Schema complexity is bounded by the weakest participant.** A field that a small
quantised model cannot reliably emit is a defect in the protocol, not in the model.
Required fields are deliberately six. Any addition MUST be justified against
metric §1.3's per-party validity rate.

### FR-3 Request Lifecycle

```
                 ┌──────────┐
   created ─────►│   open   │──────────────┐
                 └────┬─────┘              │
                      │  ▲                 │
          blocked_on  ▼  │  unblocked      │ requester withdraws
                 ┌──────────┐              │
                 │ blocked  │              │
                 └────┬─────┘              ▼
                      │            ┌──────────────┐
   assignee files     │            │  withdrawn   │ (terminal)
   a disposition      ▼            └──────────────┘
                 ┌──────────┐
                 │ resolved │ (terminal)
                 └────┬─────┘
                      │  requester objects
                      └────────► back to open
```

- A docket MUST begin with filing `000`, of `type: request`, `status: open`.
- Terminal states are `resolved` and `withdrawn`.
- A request with `act: report` requires no reply and MAY be created directly in
  `status: resolved`.

### FR-4 Assignment

- Every open docket SHOULD have exactly one `assignee` — the party responsible
  for advancing it. `assignee` may be changed by the requester or by the current
  assignee; an unclaimed docket may be claimed by any party via `act: ack`.
  Concurrent claims resolve by canonical order — the last authorised assignment
  wins, identically for every implementation.
- Absent `assignee`, the docket is **unclaimed**; any party MAY claim it by filing
  an `ack` that sets itself as assignee.
- With three or more parties, a docket without an assignee is the primary failure
  mode: every party assumes another is handling it. Implementations SHOULD surface
  unclaimed dockets prominently in `INDEX.md`.
- **There is no addressing, deliberately (r015).** S4 was originally scoped as
  *addressing and assignment*, and `to` was the addressing half. It shipped, and
  then nothing ever read it: no reducer, index, scheduler or MCP path consumed a
  recipient list, so a filing addressed to one party and assigned to another
  behaved exactly like one with no `to` at all. Worse, parties wrote `to` meaning
  *over to you* and the assignment stayed put, so the field actively absorbed the
  intent that belonged in `assignee`. 0.3 removes it and narrows S4 to assignment.
  Docket has no inbox, no notification and no per-recipient view; until something
  exists that would *act* on a recipient, addressing is a promise the format
  cannot keep. Informational addressing belongs in the body.

### FR-5 Resolution

- **Only the requester MAY close a docket.** A non-requester filing a disposition
  is *proposing* closure, not performing it.
- The requester closes by filing `type: disposition`, `status: resolved`.
- The requester MAY reject a proposed disposition by filing `act: objection`,
  returning the docket to `open`.
- A disposition SHOULD carry `evidence`; one without is conforming but weak, and
  implementations SHOULD flag it. If evidence *is* given it MUST NOT consist
  solely of filings from the disposition's own docket — evidence points outward.
  The field is deliberately not a MUST: a required field a weak party cannot fill
  produces ceremonial junk that looks like proof, observed in the r003 trial.

*Rationale: "I fixed it" is not a fact, it is a claim. This project exists
because five of seven defects in a prior experiment produced no error output — the
protocol makes the absence of proof visible rather than silent.*

### FR-6 Index

- Filings MUST be ordered by `(sequence, party)`, never by `date`: dates are
  self-asserted, and a party without a clock emits placeholders.
- State MUST be derived by one canonical reduction, so every conforming
  implementation agrees. Invalid filings are excluded from reduction and never
  silently change derived state.
- `INDEX.md` MUST be fully derivable from the filings. No state may exist only in
  the index.
- It MUST be regenerable by a single command, and regeneration MUST be idempotent.
- It SHOULD list: open dockets, assignee, age, blocked status, and unclaimed work.

### FR-7 Participant Registry

`PARTIES.md` declares each party: name, runtime, model, context budget, strengths,
relative cost, and invocation command.

This is the capability-routing input — the mechanism by which cheap local models
receive implementation work and expensive models receive review. It is Docket's
equivalent of an A2A agent card, in a format a human reads without tooling.

### FR-8 Onboarding

A party joins by being pointed at `PROTOCOL.md` from its own native context file:
`CLAUDE.md`, `QWEN.md`, `GEMINI.md`, or `AGENTS.md` (the emerging cross-vendor
convention). The protocol MUST be understandable from that document alone —
onboarding MUST NOT require tooling, credentials, or a running process.

---

## 6. Non-Functional Requirements

| ID | Requirement | Detail |
| -- | ----------- | ------ |
| NFR-1 | **Zero-dependency participation** | Any agent with file read/write and a shell can participate fully. Tooling is a convenience, never a requirement |
| NFR-2 | **Context economy** | Participating in one docket MUST NOT require reading any other docket. This is the primary constraint the format exists to satisfy |
| NFR-3 | **Human-readable at rest** | Plain Markdown. `cat`, `grep` and `git log` are first-class clients |
| NFR-4 | **Immutability** | No operation modifies an existing filing. Concurrent writers cannot destroy each other's work |
| NFR-5 | **VCS-native** | History, attribution, diffing and blame are inherited from git, not reimplemented |
| NFR-6 | **Vendor neutrality** | No requirement satisfiable by only one vendor's tooling. If a rule cannot be followed by all listed CLIs, it is not a rule |
| NFR-7 | **Weakest-participant bound** | Every MUST must be satisfiable by the least capable declared party |

---

## 7. Trust & Security Model

**Docket v0.1 provides no security guarantees.** Stating this precisely is a
requirement, not a disclaimer.

### 7.1 What is not protected

- **Identity is self-asserted.** `from: claude` is text a party typed. Any party can
  forge any other party's filings, deliberately or by imitating a file it just read.
- **No integrity.** Filings are immutable by convention. Nothing prevents a party
  with write access from rewriting or deleting one; only `git log` would show it.
- **No confidentiality.** Every party reads the whole store.
- **Git authorship is weak evidence.** Parties typically run as the same OS user.

### 7.2 The real risk: cross-agent prompt injection

A filing is **untrusted input**. An agent reading a docket is reading text authored
by another agent, which may itself have been derived from untrusted content the
other agent ingested.

- A filing may change what an agent **considers**; it MUST NOT change what an
  agent is **permitted to do**. Performing in-scope work that a filing requested
  is conforming — that is delegation, and it is the protocol's main use case.
- A conforming agent MUST NOT treat a filing as granting permission, escalating
  privilege, overriding its own rules, or vouching for an identity.
- A conforming agent MUST NOT execute, install, or exfiltrate on the authority of
  a filing alone. Such actions need exactly the confirmation they would need had
  the agent thought of them itself.
- Privileged or irreversible actions requested via Docket SHOULD require human
  confirmation, regardless of which party requested them.

This is a **confused-deputy** risk: parties have different permissions, and the
protocol makes it trivial for a low-privilege party to ask a high-privilege one to
act. The protocol cannot prevent this; agents and their harnesses must.

### 7.3 Deferred

Cryptographic signing of filings, per-party write scoping enforced by filesystem
permissions, and capability tokens are all deferred past v0.1 and recorded in §11.

---

## 8. Versioning & Extensibility

- Every filing carries `protocol: docket/<major>.<minor>`.
- A party encountering an unknown minor version MUST process the fields it
  recognises and MUST NOT discard unknown fields when quoting a filing.
- Unknown top-level fields MUST be preserved, not stripped.
- Adding an optional field is a minor bump. Adding a required field, changing an
  enum's meaning, or altering the state machine is a major bump.
- `PROTOCOL.md` is normative; this BRD is rationale. Where they disagree,
  `PROTOCOL.md` wins and the discrepancy is a bug in this document.

---

## 9. Acceptance Criteria

| #  | Check | Pass? |
| -- | ----- | ----- |
| A1 | A previously unseen agent, given only `PROTOCOL.md`, emits a schema-valid filing on its first attempt | ☐ |
| A2 | The **weakest declared party** does the same, unaided | ☐ |
| A3 | Participating in one docket requires reading no other docket | ☐ |
| A4 | `INDEX.md` regenerates from filings alone; deleting and regenerating it loses nothing | ☐ |
| A5 | Two parties writing to one docket concurrently lose no data | ☐ |
| A6 | A non-requester cannot close a docket; the attempt is visible as a proposal | ☐ |
| A7 | A full thread is reconstructable from `git log` alone | ☐ |
| A8 | Three vendors' CLIs participate in one docket without vendor-specific rules | ☐ |
| A9 | A docket reaches a terminal state without human intervention in the protocol | ☐ |

---

## 10. Reference Implementation Scope

Deliberately small; NFR-1 means none of it is required to participate.

| Tool | Purpose |
| ---- | ------- |
| `tools/docket-index` | Regenerate `INDEX.md` from filings |
| `tools/docket-mcp` | Docket over MCP (stdio JSON-RPC): six docket verbs, identity from the connection rather than any argument. Writes shell out to `docket-new`, so the MCP and CLI paths cannot drift |
| `tools/docket-init` | Scaffold a store in another repository: creates it, copies or links the protocol, registry and tools, and points each CLI's context file at them. Idempotent |
| `tools/docket-new` | Create a well-formed request or filing: allocates the docket number atomically, stamps the date, derives filename and id, enforces authority before writing, and never overwrites (exclusive create) |
| `tools/docket-lint` | Validate front matter and state-machine legality across a store |
| `tools/docket_lib.py` | The single shared model — parsing, canonical order, and the one `reduce_docket()` that both index and lint call, so they cannot disagree |

A server-mediated implementation (MCP) arrived in 0.2 as `tools/docket-mcp`. It is
**additive, never a replacement**: the store stays files, `docket-new` stays the
canonical writer, and any agent with a shell can still participate (NFR-1). MCP is
a second, typed front door for the tools that speak it. Its value is enforcement — authoritative sequence numbers, real
identity from the connection, rejecting a close from a non-requester — none of
which the file layer can guarantee.

---

## 11. Roadmap

| Phase | Contents | Status |
| ----- | -------- | ------ |
| 0 | BRD; name; storage/spec split | ✓ this document |
| 1 | `PROTOCOL.md` normative spec + `PARTIES.md` registry | ✓ |
| 2 | ~~Migrate `chatroom.md` into dockets~~ — dropped: its 11 questions are all answered, so migration would produce 11 born-resolved dockets. Kept as the historical record it is; cited in §1.1 | ✗ |
| 3 | `docket-index` + `docket-lint` reference tools | |
| 4 | Two-vendor trial; measure §1.3 metrics | |
| 5 | Three+ vendor trial; assignment and unclaimed-work behaviour | |
| 6 | Supervisor built *on* Docket: budgets, loop detection, termination | |
| 7 | MCP-mediated implementation for enforcement | ✓ `tools/docket-mcp` |
| 8 | Signed filings; per-party write scoping | |

---

## 12. Open Questions

| #  | Question | Status |
| -- | -------- | ------ |
| Q1 | Should `docket/` be hidden (`.docket/`) once tooling matures? | Open — visible while learning; the store is meant to be read |
| Q2 | Do dockets need sub-dockets (`parent_docket`), or is `refs` between dockets enough? | Open — resist until a real case demands it |
| Q3 | Is one store per repository right, or should a store span repositories? | Open — per-repo for now; cross-repo work is unproven |
| Q4 | Should `evidence` be mandatory on `disposition` rather than SHOULD? | Open — depends on whether weaker parties can satisfy it reliably (NFR-7) |
| Q5 | How are dockets archived once resolved, to keep `INDEX.md` and directory listings small? | Open — deferred until volume justifies it |

---

*End of Docket BRD v0.3 — draft. Reference implementation in `tools/`.*
