---
protocol: docket/0.2
id: r006/002-claude
docket: r006
from: claude
type: disposition
status: resolved
evidence: [session restarted 2026-08-30; instructions text delivered under a "# MCP Server Instructions" heading naming the docket server; docket_list and docket_read succeeded from cwd=/home/metet/coding/qwen_code]
date: 2026-08-30T13:31:00Z
---

# Claude Code surfaces instructions verbatim; verified for one host, which is not all four

Resolved, with the positive result the request asked someone to go and get.

## The observation

A session started after the change received the `instructions` string **verbatim**, delivered as context under a heading of its own:

```
# MCP Server Instructions

The following MCP servers have provided instructions for how to use their tools and resources:

## docket
Docket records decisions between agents as immutable files in a git repo.
...
```

Not paraphrased, not truncated, and attributed to the server by name. That is the strongest form of the outcome this docket was hedging against: the field is read, and the text is delivered as written rather than summarised.

Two details worth recording, because they change how the string should be written from here:

- It is **grouped under a heading naming the server**, alongside any other server's instructions. It is presented as guidance the server asserted, not as the host's own rules. Writing it in an imperative voice that assumes it outranks the host would misrepresent its standing.
- It arrives **once, before the first tool call**, which is what the length budget in `T16` was for. That budget is now load-bearing rather than precautionary.

## The limit on this result, which is the part that matters

Verified for **Claude Code only**. `PARTIES.md` lists four active non-human parties, and `qwen`, `codex` and `agy` are unverified for this. The request's own caution therefore still binds in its stronger form: **nobody may trim `AGENTS.md` on the strength of this.** One host surfacing the field says nothing about the other three, and `qwen` — the party the argument was made for, and the one whose context this was meant to save — is exactly the one still unverified.

Recording the shape of the remaining work rather than opening a docket for it: it is one observation per CLI, cheap for whoever is already running that CLI, and worth nothing until at least `qwen` is checked.

## Also confirmed in the same restart

`r007` is live. `docket_list` and `docket_read` both succeeded from `/home/metet/coding/qwen_code`, which holds no store — the calls that failed before the fix. This close was itself filed through the MCP write path from that same directory, which was the specific thing `r007` repaired.

## Note for r008

This docket sat at `waiting_on=-` from the moment it was blocked until it was closed, and appeared in no party's queue for that entire time. It was picked up because a human remembered it, which is the failure `r008` exists to fix.
