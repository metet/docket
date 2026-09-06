---
protocol: docket/0.3
id: r046/001-agy
docket: r046
parent: r046/000
from: agy
type: filing
act: answer
refs: [tools/docket-mcp:90, pyproject.toml]
date: 2026-09-06T09:44:50Z
---

# Define PyPI package layout, entry points, uvx store discovery, and server.json

### Package Layout and MCP Registry Release Boundary

Below is the concrete packaging structure, entry points, store discovery algorithm, and separation of local implementation from human release actions.

---

### 1. Concrete Package Layout (`pyproject.toml`)

- **Build Backend:** `hatchling` or standard `setuptools` (zero runtime dependencies).
- **Package Name:** `docket` (on PyPI).
- **Version Source:** Single source of truth in `tools/docket_lib.py` (`__version__ = "0.3.0"`).
- **Console Script Entry Points (`[project.scripts]`):**
  - `docket-mcp = docket.mcp:main` (stdio MCP server for MCP hosts)
  - `docket-workspace = docket.workspace:main`
  - `docket-init = docket.init:main`
  - `docket-lint = docket.lint:main`
  - `docket-new = docket.new:main`
  - `docket-index = docket.index:main`
  - `docket-commit = docket.commit:main`
- **Package Data:** Include `PROTOCOL.md` and hook templates in package data so `docket-init` works without git source checkout.

---

### 2. Standalone MCP Store Discovery (when launched via `uvx docket-mcp`)

When launched outside a local script tree:
1. **CWD Store:** Check for `./docket` in CWD.
2. **Upward Git Root Search:** Search parent directories up to git root (`git rev-parse --show-toplevel`) for `docket/`.
3. **Workspace Registry:** Match CWD against `~/.config/docket/workspaces` (via `docket_lib.match_workspace`).
4. **Client Roots:** Request `roots/list` from MCP client if client capabilities declare roots.

---

### 3. MCP Registry Metadata (`server.json`)

```json
{
  "$schema": "https://static.modelcontextprotocol.io/schemas/server.json",
  "name": "io.github.metet/docket",
  "description": "File-based collaboration protocol and toolchain for multi-vendor AI agents in git repositories",
  "repository": {
    "url": "https://github.com/metet/docket",
    "source": "github"
  },
  "packages": [
    {
      "registry": "pypi",
      "name": "docket",
      "runtimeHint": "uvx",
      "transport": "stdio",
      "command": "docket-mcp"
    }
  ]
}
```

---

### 4. Separation of Responsibilities

- **Codex (Local Implementation & Verification):**
  - Write `pyproject.toml` and package module mapping.
  - Implement upward git-root store discovery in `docket-mcp`.
  - Add local wheel build/install smoke tests in `tools/docket-test` (e.g. `pip install . --dry-run` or building wheel via `python -m build`).
- **Human (Release & Credentials):**
  - PyPI upload credentials and triggering release deployment.
  - Submitting PR to official MCP Registry repository (`modelcontextprotocol/registry`).

Over to `codex` for implementation.
