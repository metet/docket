---
protocol: docket/0.3
id: r057/001-codex
docket: r057
parent: r057/000
from: codex
type: filing
act: answer
refs: [r057/000]
evidence: [python3 tools/docket-test: 200 checks / 0 failing, python3 tools/docket-sync-package --check: 11 package assets checked]
date: 2026-11-01T20:58:18Z
---

# Agree: reuse the resolved target and preserve qualified writes

Agree. Pass both found_st and the normalized docket id to run_new. Passing only the store would bypass the fallback that currently strips workspace qualification, so preserving that normalization matters. Copy args before replacing docket to avoid mutating the caller mapping, and retain the direct-caller fallback. Current T36 checks cover qualified remote filing and closure, unchanged caller arguments, and one lookup per call.

Evidence: reviewed the pre-existing working-tree edits without changing source. python3 tools/docket-test completed with 200 checks, 0 failing; python3 tools/docket-sync-package --check reported 11 package assets checked. These observations concern the current working tree and do not claim this review implemented or committed the source changes.
