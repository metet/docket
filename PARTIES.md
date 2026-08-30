# Parties

Participants in this Docket store. Your `from:` field MUST match a **name** below.

This file is the routing input: send judgement, review and root-cause work to
expensive parties; send bulk implementation to cheap ones. Cost is the reason the
distinction exists.

> **Not to be confused with a repository-root `AGENTS.md`**, which some CLIs read
> as their own instruction file. The registry lives here, inside the store.

---

## Registry

| name | runtime | model | context | cost | strengths |
| --- | --- | --- | --- | --- | --- |
| `qwen` | Qwen Code → Ollama @ `localhost:11434` | `Qwen3.6-35B-A3B-UD-Q4_K_XL` (4-bit, ~3B active) | small — confirm in server config | ~zero (local) | Peripheral implementation only — single-file edits, verifiable dependency-light work. **Not** the protocol, the store, or the toolchain; see below |
| `claude` | Claude Code | Claude Opus 5 | large | $$ | Review, root-cause analysis, spec and protocol work |
| `codex` | Codex CLI | `gpt-5.6-sol` at `model_reasoning_effort = max` | *unverified* | $$ | *unverified* |
| `agy` | Antigravity CLI (`agy` 1.1.22) | `Gemini 3.7 Flash (High)` — default, switchable with `--model` | *unverified* | ? | *unverified* |
| `openclaw` | openclaw | *unverified — fill in* | *unverified* | ? | *unverified* |
| `human` | terminal | — | — | — | Authority, tiebreaker, scheduler, anything irreversible |

Rows marked *unverified* are placeholders. Fill them in before routing work to
that party — do not guess a party's context budget, because under-estimating it
wastes money and over-estimating it silently truncates its input.

## Invocation

| name | command |
| --- | --- |
| `qwen` | `qwen -p "<prompt>"` |
| `claude` | `claude -p "<prompt>"` |
| `codex` | `codex exec "<prompt>"` *(verify)* |
| `agy` | `agy -p "<prompt>"` |
| `openclaw` | *(verify)* |

Docket is **pull-only** — nothing here wakes an idle party. Something outside the
protocol, a human or a supervisor, decides when a party runs. These commands are
how that is done.

## Capability asymmetry

Parties are deliberately unequal, and this is a design input rather than a problem
to be normalised away:

- **`qwen` is the weakest declared party.** Per NFR-7, every MUST in `PROTOCOL.md`
  must be satisfiable by it. A field `qwen` cannot reliably emit is a defect in the
  protocol, not in `qwen`.
- **Context budgets differ by an order of magnitude.** A filing that is a light
  skim for `claude` may consume most of `qwen`'s usable window. This is why
  `PROTOCOL.md` §5 forbids requiring a read of the whole store.
- **Permission models differ per CLI.** Each will prompt differently before writing
  into `docket/`. Pre-authorise that path per tool, or every turn costs an approval.
- **`qwen` is not routed work that decides correctness.** Nothing touching
  `PROTOCOL.md`, `docket_lib.py`, the validity model, or how the store reports its
  own state. Cost is not the deciding input here: a wrong answer in the layer
  everything else is checked against is not caught by the layer it broke, and the
  repair costs more than the implementation saved. Route it to `claude`.

  This is a decision by `human`, taken after `qwen` filed `mindmap/r002/002-qwen.md`
  by hand and invalid. It follows from the asymmetry above rather than sitting
  beside it: a party that cannot reliably emit six front-matter fields is not the
  party to be given the code that decides whether those fields are correct.

- **`qwen`'s output is triaged by `claude`, not re-worked by `qwen`.** When a
  filing or a change from `qwen` is wrong, the correction goes to `claude`.
  Handing the repair back to the party that produced the fault risks compounding
  it, and in an append-only store a compounded fault cannot be taken back.

## Onboarding a new party

1. Add a row above, with a name nothing else uses.
2. Point the tool's own context file at the protocol — one line is enough:
   `Read docket/PROTOCOL.md before writing to docket/.`

   **Two files cover four tools, and adding more is harmful.** Verified against
   the installed CLIs: `AGENTS.md` is read by Codex, Gemini CLI **and** Qwen
   Code; `CLAUDE.md` is read by Claude Code (and also by Qwen Code, which is why
   it guards itself by name). Qwen Code reads *all* of `AGENTS.md`,
   `CLAUDE.md`, `CONTEXT.md`, `GEMINI.md` and `QWEN.md` — so creating a separate
   `QWEN.md` and `GEMINI.md` saying the same thing would make the
   smallest-context party load the same guidance three or four times before
   reading any code. That is NFR-7 violated in the setup rather than the
   protocol.

   Add a per-tool file only when a party needs guidance that genuinely differs.
3. Pre-authorise writes to `docket/` in that tool's permission settings.
4. Verify: ask it to file one `act: report` docket. If that filing is schema-valid
   with no correction, onboarding worked — this is acceptance criterion A1.

## Retired

Parties are **never removed from this file**. Filings are immutable, so deleting a
party would invalidate its entire history — every filing naming it would fail
validation on a registry edit, which is a mutable document breaking an immutable
one. Move a departing party to the table below instead.

A retired party's past filings stay valid. It MUST NOT file anything new, and
implementations SHOULD warn if it does.

| name | retired | note |
| --- | --- | --- |
| `gemini` | 2026-08-30 | Gemini CLI cannot authenticate — `oauth-personal` returns IneligibleTierError, the free tier having been withdrawn for that client. Superseded by `agy`, which reaches the same models through Antigravity. `r001/001-gemini` was filed before this row existed and was in fact produced by `agy`; see `r001/002-claude-report`. |

## Trust

Every name here is **self-asserted**. Docket has no authentication: any party can
write any other party's name in a `from:` field, deliberately or by imitating a
file it just read. Git authorship does not help — all parties typically run as the
same OS user.

Treat this registry as a directory, never as proof of who wrote something. See
`PROTOCOL.md` §7.
