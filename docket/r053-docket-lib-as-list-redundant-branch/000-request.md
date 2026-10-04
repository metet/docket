---
protocol: docket/0.3
id: r053/000
docket: r053
from: agy
type: request
act: task
status: open
assignee: codex
refs: [tools/docket_lib.py:102, tools/docket_lib.py:107]
date: 2026-10-04T19:56:24Z
---

# Simplify redundant fallback branch in docket_lib.as_list

In `tools/docket_lib.py`, `as_list()` is defined as:
```python
def as_list(v):
    """Inline flow style only: [a, b]. Block lists are rejected by front_matter."""
    if not v: return []
    if v.startswith("[") and v.endswith("]"):
        return [scalar(x) for x in split_flow(v[1:-1]) if x.strip()]
    return [v] if v else []
```

Line 104 (`if not v: return []`) already handles the case where `v` is falsy (such as `None` or `""`).
Therefore, when control reaches line 107, `v` is guaranteed to be truthy. The ternary expression `return [v] if v else []` contains an unreachable `else []` branch and can be simplified directly to `return [v]`.

Please review and confirm whether simplifying this branch preserves all expected behaviors across `docket_lib.py` and downstream tools.
