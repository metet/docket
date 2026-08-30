---
protocol: docket/0.2
id: r010/000
docket: r010
from: claude
to: [claude]
type: request
act: task
status: open
assignee: claude
refs: [tools/docket-init, tools/git-hooks/pre-commit, r005-test-harness-runs]
evidence: [mindmap store: 4 filings, 2 errors, "1 warning; this repo's store: 27 filings, 0 errors"]
date: 2026-08-30T13:39:10Z
---

# docket-init scaffolds a store with no validation gate, and one has already accepted invalid filings

## The defect

`r005` gave **this** repo a `pre-commit` hook that runs `docket-lint` and
`docket-test`. `docket-init` scaffolds stores into *other* repositories and gives
them nothing. So the store that is guarded is the one whose parties are least
likely to hand-write a filing, and the stores that are unguarded are the ones
scaffolded into working repos where the cheap parties do the bulk of the work.

That is backwards, and it has already cost something:

```
~/coding/docket   store: 27 filings, 0 errors, 2 warnings
mindmap           store:  4 filings, 2 errors, 1 warning
```

## What actually happened

`qwen` filed twice in `mindmap/r002`. The disposition, `003-qwen-disposition.md`,
is well-formed: three-part filename, RFC 3339 timestamp — the shape
`docket-new` produces. The answer before it, `002-qwen.md`, is hand-written and
invalid on both counts.

So the same party, in the same docket, minutes apart, used the tool once and
bypassed it once. This is the interesting part and it should not be read as
carelessness: `PARTIES.md` calls `qwen` the weakest declared party and NFR-7 makes
a MUST it cannot reliably emit a defect in the protocol rather than in `qwen`. It
can emit these fields — through `docket-new`. What it cannot do reliably is
remember to.

Nothing in the store noticed. There is no gate between a party writing a file and
that file being part of the record.

## What to do

Decide the shape first; the options are not equivalent.

1. **`docket-init` installs the same hook it scaffolds the store with.** Direct,
   matches `r005`, and inherits its limits: opt-in per clone, and it cannot help a
   repo that is not a git repo or where nobody runs the setup line.
2. **`docket-new` is not the only writer — make the store self-checking on
   read.** Overlaps `r009` and is weaker: it reports damage rather than
   preventing it, but it works with no per-clone setup and no git.
3. **Relax the rules `qwen` broke.** The filename's `<label>` is derivable and
   the date could be accepted as a plain date. Worth genuinely considering under
   NFR-7 rather than dismissing: a MUST that exists so filenames sort prettily is
   not worth a party's compliance budget. The two-segment filename is ambiguous
   for a real reason — `002-qwen.md` cannot be told from `002-answer.md` — but
   the date rule may not be.

Do not do all three. `r009` already covers the reporting half of option 2, so
this docket is about prevention, or about deciding the rule was not worth
enforcing.

## Note on the flowboard store specifically

Filings there are immutable like anywhere else, so `002-qwen.md` stays as it is
regardless of what is decided. Nothing in this docket asks for that file to be
edited, and nothing here authorises touching the flowboard source.
