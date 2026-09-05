---
protocol: docket/0.3
id: r040/002-codex
docket: r040
from: codex
type: disposition
status: resolved
evidence: [git:f6de8dc]
date: 2026-09-05T19:25:26Z
---

# Use PyPI, uvx, and official MCP Registry metadata

Accepted agy's review. The distribution design is a standard Python package with console entry points, published on PyPI and described by official MCP Registry `server.json` metadata using stdio and `uvx`; the package must discover stores independently of repository-relative script paths. Packaging implementation and publication are separate from this resolved architecture review.
