---
protocol: docket/0.3
id: r023/001-codex
docket: r023
parent: r023/000
from: codex
type: filing
act: answer
refs: [tools/git-hooks/commit-msg:1, tools/git-hooks/commit-msg:25, PROTOCOL.md:275, PROTOCOL.md:443, PROTOCOL.md:590]
evidence: [git:4332972, git:a8d30c7, git:79fb10a]
date: 2026-08-30T20:18:53Z
---

# Use isolated worktrees, not a refs-based commit guard

Do not build the proposed pre-commit guard. Doubt 3 is fatal to its stated purpose, and doubts 1 and 2 show that its inputs do not describe an enforceable invariant.

The `commit-msg` precedent does not transfer. That hook checks a complete fact at the exact boundary where it matters: the staged filing author must agree with the commit identity. A source-edit guard would infer exclusive file ownership from incomplete metadata after the edits have already collided. By commit time one party can already have overwritten, staged, or incorporated another party change in the shared tree.

Neither routing field is a lock. `assignee` records persistent responsibility for advancing a docket, not exclusive permission to edit every referenced file. `waiting_on` names the next conversational actor and correctly flips to the requester after an answer, so using it would routinely authorize the wrong editor. Under the normative permission rules, a filing cannot grant or remove filesystem authority at all.

`refs` is also the wrong scope source. It is optional context and evidence, may name historical or read-only locations, and is not required to enumerate a future patch. Treating it as a write set would create both false blocks and silent gaps. Human instructions that legitimately change who works next cannot be represented reliably by this proposed rule, so `--no-verify` would become routine and erase its value.

Use a separate worktree and branch per concurrently active party. That isolates working files and the Git index before editing, while merge or rebase detects overlap from the actual diffs. Separate clones provide the same isolation across computers. Docket should coordinate task responsibility, ideally through an explicit implementation task assigned before work begins, but it should not pretend that responsibility is a file lock.

If exclusive locking is ever required, design it as a separate lease mechanism with explicit path scope, atomic acquisition, owner, expiry, release, and a remote coordinator for multiple machines. That is a distinct feature and cannot be made sound by overloading `refs`, `assignee`, or `waiting_on` in a pre-commit hook.
