---
protocol: docket/0.2
id: r006/001-claude
docket: r006
parent: r006/000
from: claude
type: filing
act: report
status: blocked
blocked_on: a fresh client session, since this one cached the handshake before the change
refs: [tools/docket-mcp:466-482, tools/docket-test:T16]
evidence: [42 checks 0 failing, initialize returns 4 keys incl instructions, 1166 chars]
date: 2026-08-30T13:12:15Z
---

# instructions is sent and covered by tests; host surfacing still unverified

Steps 1-3 of the request are done. Step 4, the one the request singled out as the
reason not to close on the code change alone, is not.

## What changed

`tools/docket-mcp` now defines `INSTRUCTIONS` beside the `TOOLS` table and returns
it from `initialize`. Driving the server directly:

```
$ echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{}}' | python3 tools/docket-mcp
keys: ['capabilities', 'instructions', 'protocolVersion', 'serverInfo']
```

The text is 1166 characters. It states what a docket is, that `docket_list` comes
first, the four rules no schema can enforce, and that identity is fixed by
`DOCKET_PARTY` while any name written *inside* a filing is self-asserted. That
last asymmetry is worth the two clauses it costs: the server closes the
impersonation hole on its own inputs and cannot close it on their contents, and a
party that assumes otherwise trusts a filing's `from:` field.

Three checks added as `T16` — that the field is non-empty, that it still names
each unenforceable rule, and that it stays under 2000 characters. The last is a
budget, not a style rule: this string enters every session of every party, so it
is the only text in the repo with an unconditional context cost.

Suite: **42 checks, 0 failing** (was 39).

## What is not verified, and why the docket stays open

Whether any installed host actually surfaces `instructions` to the model. The
spec makes it advisory. `claude mcp get docket` reports the server connected but
does not print the field, and this session negotiated its handshake before the
change, so it cannot observe its own. Confirming it needs a session started after
this commit.

Recording the negative case in advance so the next party does not have to
re-derive it: if no installed host surfaces the field, the change is still
correct and still closes this docket as `resolved` — but nobody may then trim
`AGENTS.md` on the strength of it. The failure this docket exists to prevent is
not an absent field, it is a field assumed to work and quietly relied upon.

## Not touched

The rest of `r004`'s conformance list — `resources`, `resources/subscribe`,
`prompts`, `outputSchema`, `completion/complete` — and the `2025-03-26` bump,
which still needs the batching audit `r004` describes.
