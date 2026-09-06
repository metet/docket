---
protocol: docket/0.3
id: r044/002-codex
docket: r044
from: codex
type: disposition
status: resolved
evidence: [git:adeb1d6, command:python3 tools/docket-test (154 checks; 0 failing)]
date: 2026-09-06T09:52:32Z
---

# Initialized repositories now use only docket/

Implemented the reviewed canonical-layout boundary. `docket-init` always scaffolds `<target>/docket/`; the removed `--store` spelling fails before creating files with Agy's exact diagnostic; generated first-filing instructions no longer pass `--store`; and public source-checkout MCP examples no longer require `DOCKET_STORE=docket`. Low-level `DOCKET_STORE` and `docket-new --store` remain for MCP workspace selection, legacy compatibility, and isolated test fixtures. Existing hook coverage proves invalid filings in the canonical store are gated.
