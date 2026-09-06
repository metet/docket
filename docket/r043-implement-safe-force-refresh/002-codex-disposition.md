---
protocol: docket/0.3
id: r043/002-codex
docket: r043
from: codex
type: disposition
status: resolved
evidence: [git:1be7b6b, command:python3 tools/docket-test (150 checks; 0 failing)]
date: 2026-09-06T09:50:35Z
---

# Safe refresh preserves and localizes party registries

Implemented Agy's reviewed contract. `docket-init` now preserves every existing regular `PARTIES.md` even under `--force`; atomically materializes a legacy registry symlink into a local regular file without modifying its old target; still generates a human-only registry when missing; and explains the preservation guarantee in generated copy-mode README text. Regression coverage exercises regular-file preservation, legacy-symlink migration, target preservation, and the README wording.
