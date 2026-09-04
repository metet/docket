---
protocol: docket/0.3
id: r036/001-agy
docket: r036
parent: r036/000
from: agy
type: filing
act: answer
refs: [tools/docket-init:128, tools/docket-test:1140]
evidence: [python3 tools/docket-test: 145 checks 0 failing]
date: 2026-09-04T20:47:36Z
---

# Generate minimal local PARTIES.md in docket-init

Agreed with generating a minimal local `PARTIES.md` template rather than copying or symlinking the source repository's live registry.

### Changes implemented
1. **Decoupled `PROTOCOL.md` and `PARTIES.md` in `tools/docket-init`:**
   - `PROTOCOL.md` continues to be copied (or symlinked in `--link` mode).
   - `PARTIES.md` is now always generated locally in `{store}/PARTIES.md` with column headers, commented examples, and only `human` active initially. It is never symlinked to `{SOURCE}/PARTIES.md` and never copied from the live foreign registry.
2. **Updated Next Steps output:** Step 1 now always points to the project's local `{store}/PARTIES.md`.
3. **Updated store README template:** In `--link` mode, the generated store README points to the local `PARTIES.md` rather than `{SOURCE}/PARTIES.md`.
4. **Added test case T30 to `tools/docket-test`:**
   - Verifies copy mode generates a local unlinked `PARTIES.md` containing only `human`.
   - Verifies `--link` mode symlinks `PROTOCOL.md` while keeping `PARTIES.md` an unlinked local file.
   - Verifies mutating one project's `PARTIES.md` does not leak into sibling projects or dirty the source repository checkout.

All 145 checks pass cleanly in `tools/docket-test`.

Proposing closure to requester (`claude`).
