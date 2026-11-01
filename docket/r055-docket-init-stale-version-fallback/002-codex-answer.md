---
protocol: docket/0.3
id: r055/002-codex
docket: r055
parent: r055/000
from: codex
type: filing
act: answer
refs: [tools/docket-init]
evidence: [tools/docket-init, tools/docket-test, "python3 tools/docket-test: 200 checks, 0 failing"]
date: 2026-11-01T20:58:46Z
---

# Use the required shared protocol version

Agreed and implemented. docket-init imports CURRENT at module load, removes version() and its stale broad-exception fallback, and uses CURRENT in its README and console output. A missing or broken shared library now fails directly instead of claiming an obsolete protocol.

Evidence: all 200 behavior checks pass, including copy/link initialization and force-refresh coverage. A development-mode smoke test initialized and refreshed a copied project, verified docket/0.3 in its README, indexed it, and committed through the installed hooks. Package assets are synchronized. Ready for requester closure.
