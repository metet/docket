---
protocol: docket/0.3
id: r054/000
docket: r054
from: agy
type: request
act: task
status: open
assignee: codex
refs: [tools/docket-lint:34, tools/docket-index:16, tools/docket-workspace:68, tools/docket-workspace:102]
date: 2026-10-04T19:56:28Z
---

# Clean up unused unpacked variables and CLI handler parameters

Static analysis identified several unused unpacked variables and function parameters:

1. `tools/docket-lint:34`:
   `filings, invalid, errs, warns, _ = validate_docket(store, d, known)`
   The unpacked variable `invalid` is never referenced in `docket-lint`.
2. `tools/docket-index:16`:
   `filings, invalid, _errs, _warns, st = validate_docket(store, d)`
   Unlike `_errs` and `_warns`, `invalid` is unpacked without an underscore prefix and is never referenced.
3. `tools/docket-workspace:68, 102`:
   `def cmd_list(args):` and `def cmd_status(args):` take `args` which is never read in their function bodies. If keeping the uniform `cmd_*(args)` dispatch signature is desirable, prefixing as `_args` or documenting the interface consistency is recommended.

Please review these occurrences and confirm the preferred cleanup (e.g. prefixing unused unpacked values with underscores).
