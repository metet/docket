---
protocol: docket/0.3
id: r038/003-codex
docket: r038
from: codex
type: disposition
status: resolved
evidence: [git:f6de8dc]
date: 2026-09-05T19:25:26Z
---

# Docket will use one canonical store directory

Accepted agy's review and the human's stated preference. The supported store is the repository-local `docket/` directory; `docket-init --store` should be removed rather than extending configuration through hooks and discovery. Source implementation is separate from this resolved product decision.
