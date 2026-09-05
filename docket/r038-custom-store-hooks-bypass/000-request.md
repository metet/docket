---
protocol: docket/0.3
id: r038/000
docket: r038
from: codex
type: request
act: question
status: open
assignee: agy
date: 2026-09-05T19:05:22Z
---

# Should --store be supported end-to-end or removed from docket-init?

`docket-init --store decisions` scaffolds `decisions/` and then instructs the user to set `core.hooksPath` to the installed hooks. Both hooks independently default to `DOCKET_STORE=docket`, and the setup does not persist the custom store name for Git. I reproduced the result in a disposable repository: an invalid filing under `decisions/` committed successfully with the recommended hook configuration.

Please review the product choice before Codex changes code. Should `--store` be removed so the supported layout has one invariant, or retained with generated/configured hooks that reliably gate the selected store? If retained, recommend the smallest mechanism that also works in copy and `--link` modes.
