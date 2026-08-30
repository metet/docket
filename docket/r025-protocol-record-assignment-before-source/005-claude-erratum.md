---
protocol: docket/0.3
id: r025/005-claude
docket: r025
supersedes: r025/004-claude
corrects: [evidence]
from: claude
type: filing
act: erratum
evidence: [git:b488d89, git:7289e49, PROTOCOL.md:485, docs/PROCESS_FLOW.md:240, command:python3 tools/docket-test -> 133 checks, 0 failing]
date: 2026-08-30T21:29:33Z
---

# Erratum: the disposition's evidence pointed only inward

`004-claude` cited only filings from r025 itself, which lint correctly refuses: a
disposition's evidence must point outward, or it proves a conclusion by quoting
the argument that reached it.

Corrected to the commits the design was settled in, the two files the task
dockets change, and the suite result standing at the time of closure. The
substance of the disposition is unchanged.

Worth noting the rule earned its keep here. I closed a design docket citing three
filings from that same docket as proof it was settled, and every one of them was
written in the conversation being summarised.
