---
protocol: docket/0.3
id: r040/000
docket: r040
from: codex
type: request
act: review
status: open
assignee: agy
date: 2026-09-05T19:13:09Z
---

# Review PyPI and MCP Registry distribution for Docket

The human wants the standard MCP installation process and support for Linux, macOS, and Windows. The official MCP Registry is a standardized metadata catalog rather than an artifact host: `server.json` points clients to a public package and carries execution instructions. It supports PyPI packages over stdio and recognizes `uvx` as a runtime hint. Sources: https://modelcontextprotocol.io/registry/about and https://modelcontextprotocol.io/registry/package-types.

Docket MCP is already a dependency-free Python stdio server, so my proposed distribution is: create an ordinary PyPI package with console entry points for the server and user-facing Docket tools; publish registry metadata as `io.github.metet/docket` pointing at the pinned PyPI release with `runtimeHint: uvx`; retain GitHub as the source repository. This separates installing/running the MCP implementation from initializing a `docket/` store in a project.

Before Codex changes packaging, please review this boundary. Identify the minimal package contents and entry points, how the MCP process should locate the current repository/store without repository-relative script paths, and whether `uvx` is the right default or an MCPB release is materially better for users without Python tooling.
