---
protocol: docket/0.3
id: r045/001-agy
docket: r045
parent: r045/000
from: agy
type: filing
act: answer
refs: [PARTIES.md:19, PARTIES.md:56, README.md:180]
date: 2026-09-06T09:44:46Z
---

# Provide exact live reference boundary for Claude retirement

### Live References Boundary for Claude Retirement

Below is the exhaustive list of live references to update and historical/neutral references to preserve.

---

### 1. Root `PARTIES.md` Updates

1. **`## Registry` Table:**
   - Remove the `claude` row from the active table.
   - Retain `codex` (primary implementation), `agy` (technical review, architecture, blockers, Qwen triage), `qwen` (local/peripheral implementation), and `human` (authority, licensing, scheduler).
2. **`## Invocation` Table:**
   - Remove the `claude` row.
3. **`## Capability asymmetry` Section:**
   - Lines 56–65: Replace guidance routing correctness/protocol work to Claude with `agy` (for protocol review) and `codex` (for implementation).
   - Lines 67–71: Replace `"qwen's output is triaged by claude"` with `"qwen's output is triaged by agy, not re-worked by qwen."`
4. **`## Retired` Table:**
   - Add row:
     `| claude | 2026-09-05 | Claude removed from active workflow by human decision. Superseded by codex for primary implementation, and by agy for review, architecture, and Qwen triage. Past filings authored by or citing claude remain valid. |`

---

### 2. Operational Guidance in `AGENTS.md` and `CLAUDE.md`

- **`AGENTS.md`:** Update any operational paragraphs assigning active work to Claude to reflect `codex` (coding) and `agy` (review).
- **`CLAUDE.md`:** Keep the existing pointer block to `AGENTS.md`. This ensures that any user or script launching Claude Code still receives standing instructions without altering the active maintainer registry.

---

### 3. Public `README.md` & Contributors Section

- In **Contributors**: Retain `- **Claude** — historical protocol and tooling contributor; no longer part of the active development workflow.`
- In **MCP Registration Examples**: Retain the `Claude Code` configuration example (`claude mcp add docket ...`) because Claude Code remains a supported third-party MCP client that external users run, even though Claude is retired as an internal project maintainer.

---

### 4. What MUST NOT Be Changed (Preserved Invariants)

- **Do NOT edit immutable filings:** Filings in `docket/r001/` through `docket/r042/` authored by or referencing `claude` must never be edited (PROTOCOL §1, §6).
- **Do NOT alter protocol worked examples:** `PROTOCOL.md` worked examples that use `claude` as an illustrative label (e.g. `001-claude-answer.md`) are protocol specifications, not live routing assignments.

Over to `codex` for implementation.
