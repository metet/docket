# Docket

A file-based protocol that lets AI agents from different vendors collaborate through plain files in a git repo — no server, no shared SDK, no vendor lock-in.

---

## Architecture & Documents

- **[`PROTOCOL.md`](PROTOCOL.md)**: The normative specification. Defines the state machine, filing types, lifecycle transitions, and strict YAML front-matter subset.
- **[`PARTIES.md`](PARTIES.md)**: The registry of participants. Distinguishes CLI runtimes from models and records active/retired agent identities.
- **[`helpme.md`](helpme.md)**: Guide to Docket roles — explains the difference between the immutable owner (`requester`), the mutable `assignee`, and the dynamically derived `waiting_on`.
- **[`AGENTS.md`](AGENTS.md)**: Instructions and behavioral constraints for autonomous agents.
- **[`BRD.md`](BRD.md)**: Business and technical rationale explaining design choices.

---

## Installation & Requirements

Docket has **zero external dependencies** — it relies solely on Python's standard library and Git.

- **Python:** Standard library only. Syntax floor is Python 3.8+ (due to the walrus operator in `tools/docket-new`), tested on Python 3.13+.
- **Git:** Any modern Git supporting `core.hooksPath`.

The currently available installation runs from a GitHub source checkout. A
packaged PyPI release and official MCP Registry entry are being prepared, but
have not been published yet. Linux is the verified platform today; macOS and
native Windows support are targets, not current compatibility claims.

### Two-Tier Tool Layout

Docket tools are organized into two groups:

1. **Source / Shared Toolchain** (run from the Docket source clone across projects):
   - `tools/docket-mcp`: Stdio JSON-RPC 2.0 MCP server for agent integration.
   - `tools/docket-workspace`: Workspace registry manager for multi-repo coordination.
   - `tools/docket-test`: Self-contained regression test suite.

2. **Per-Repository Scaffolded Toolchain** (copied by `docket-init` into `<repo>/tools/`):
   - `tools/docket-new`: Filing creation with atomic number reservation.
   - `tools/docket-lint`: Schema and state-machine validator.
   - `tools/docket-index`: Rebuilding `INDEX.md` turn-tracker tables.
   - `tools/docket-commit`: Attribution-preserving Git commit wrapper (`--from <party>`).
   - `tools/docket_lib.py`: Core protocol library.
   - `tools/git-hooks/`: Tracked git hooks (`pre-commit` and `commit-msg`).

---

## Getting Started: Scaffolding a Repository

To add Docket to any code repository:

```bash
git clone https://github.com/metet/docket.git
python3 docket/tools/docket-init /path/to/my-project
```

Next steps in the initialized repository:

1. **Configure participants:** Edit `docket/PARTIES.md` to list the agents and humans collaborating in that repository.
2. **Pre-authorise writes:** Configure agent CLIs to allow writes to `docket/` and set their identity with `DOCKET_PARTY=<party>`.
3. **Gate commits:** Run `git config core.hooksPath tools/git-hooks` so Git validates filings on commit.
4. **File your first docket:**
   ```bash
   tools/docket-new request --from <you> --slug my-first-task --title "Initial task" --act question
   ```

### What a “store” is

A Docket store is just the `docket/` directory inside a project. It contains
`INDEX.md`, `PARTIES.md`, the number reservations in `.seq/`, and the immutable
docket filings. It is not a remote service, database, account, or shared global
directory.

Use the default name `docket/`. Custom store names are not needed for ordinary
projects and are not part of the recommended setup while their discovery and Git
hook behavior is under review.

---

## Tools

Docket includes a zero-dependency reference toolchain in `tools/`:

| Tool | Purpose |
| :--- | :--- |
| **`tools/docket-workspace`** | Manage trusted project folders: add, remove, list, and view cross-project dashboards. |
| **`tools/docket-mcp`** | Stdio JSON-RPC 2.0 MCP server exposing Docket verbs (`docket_list`, `docket_read`, `docket_open`, `docket_file`, `docket_close`, `docket_protocol`). |
| **`tools/docket-new`** | Atomically allocate docket numbers, stamp dates, derive filing IDs, and create immutable markdown files. |
| **`tools/docket-init`** | Scaffold a new Docket store in any code repository (supports `--link` symlink mode). |
| **`tools/docket-index`** | Regenerate `docket/INDEX.md` turn-tracker and status tables from filings. |
| **`tools/docket-lint`** | Validate schema, front matter, and state-machine legality across a store. |
| **`tools/docket-test`** | Self-contained regression test suite (145 automated behavioral checks). |
| **`tools/docket-commit`** | Commit as a named party: sets the git author for that one invocation and records a `Docket-Party:` trailer. |
| **`tools/git-hooks/`** | Tracked git hooks. `pre-commit` runs the lint and the suite; `commit-msg` refuses a commit whose declared party contradicts the filings it carries. Opt in per clone with `git config core.hooksPath tools/git-hooks`. |

### Running the checks

```bash
python3 tools/docket-lint    # schema and state-machine legality
python3 tools/docket-test    # 145 behavioural checks
```

To have git run both before every commit, once per clone:

```bash
git config core.hooksPath tools/git-hooks
```

The hook gates on exit status, not output: `docket-lint` carries standing
warnings deliberately (see `r003/003`), and those never block a commit. Bypass a
single commit with `git commit --no-verify`.

---

## Trusted Workspaces & Multi-Project Setup

Docket stores are **per-repository** (`<repo>/docket/`), keeping bug reports, decisions, and resolutions versioned directly alongside the code they describe.

To securely manage multiple repositories without blind filesystem crawling, Docket uses an explicit **allowlist configuration**.

### 1. The Workspaces Config File

Config location:  
`~/.config/docket/workspaces` *(plain text, one absolute path per line)*  
or `~/.config/docket/workspaces.json`

Example:
```text
# Docket trusted workspaces (one path per line)
/home/metet/coding/docket
/home/metet/coding/qwen_code/mindmap
```

### 2. Managing Workspaces (`docket-workspace`)

Use `tools/docket-workspace` to easily register and inspect approved folders:

```bash
# Add a repository (defaults to current directory if omitted)
tools/docket-workspace add /path/to/my-project
tools/docket-workspace add .

# Remove a repository
tools/docket-workspace remove /path/to/my-project

# List all trusted workspaces and their current docket status
tools/docket-workspace list

# View a consolidated dashboard of open work across all workspaces
tools/docket-workspace status
```

**Example dashboard output:**
```text
=== [docket] /home/metet/coding/docket ===
  r004-session-handoff         status=open  assignee=claude  waiting_on=claude

=== [mindmap] /home/metet/coding/qwen_code/mindmap ===
  r002-palette-drag-drop       status=open  assignee=codex  waiting_on=codex
```

---

## MCP Server Integration (`docket-mcp`)

`tools/docket-mcp` allows MCP-enabled agents (Claude Code, Qwen Code, Cursor, Codex) to interact using structured tool calls rather than raw shell scripts:

Until the packaged MCP release is published, configure clients to launch
`tools/docket-mcp` from the source checkout, as in the examples below. Do not
install a similarly named third-party package and assume it is this project.

### Automatic Store Resolution
When `DOCKET_STORE="docket"` (relative), the MCP server automatically checks if the agent's current working directory matches an approved workspace in `~/.config/docket/workspaces`. If matched, it routes all tool calls to `<workspace>/docket/`.

### Automatic Cross-Workspace Turn Detection
Even when an agent is running inside a specific repository, `docket_list` automatically checks all other trusted workspaces registered in `~/.config/docket/workspaces`. If there is any open docket waiting on that agent in another project, `docket_list` surfaces it:
```text
r004-session-handoff  status=open  assignee=claude  waiting_on=claude

1 waiting on you (codex) in other trusted workspaces:
  [mindmap] r002-palette-drag-drop  status=open  waiting_on=codex  (in /home/metet/coding/qwen_code/mindmap)
```

Agents can read or file directly to dockets in other trusted workspaces using their slug or workspace prefix (e.g. `docket_read({"docket": "mindmap/r002"})` or `docket_read({"docket": "r002-palette-drag-drop"})`).

### Cross-Workspace Queries
Agents can query open work across all approved projects at once by setting `workspace="all"`:
```json
{
  "name": "docket_list",
  "arguments": { "workspace": "all" }
}
```

### Registration Examples
* **Claude Code:**
  ```bash
  claude mcp add docket -e DOCKET_PARTY=claude -e DOCKET_STORE=docket -- python3 /path/to/tools/docket-mcp
  ```
* **Qwen Code (`~/.qwen/settings.json`):**
  ```json
  "tools": {
    "visible": [
      "mcp__docket__docket_list",
      "mcp__docket__docket_read",
      "mcp__docket__docket_open",
      "mcp__docket__docket_file",
      "mcp__docket__docket_close",
      "mcp__docket__docket_protocol"
    ]
  },
  "mcpServers": {
    "docket": {
      "command": "python3",
      "args": ["/path/to/tools/docket-mcp"],
      "env": {
        "DOCKET_PARTY": "qwen",
        "DOCKET_STORE": "docket"
      },
      "trust": true
    }
  }
  ```

---

## Contributors

- **metet** — creator and maintainer.
- **Codex** — current implementation contributor.
- **agy** — implementation and technical-review contributor.
- **Claude** — historical protocol and tooling contributor; no longer part of
  the active development workflow.
- Other registered Docket parties have contributed filings and review.

Agent commits use self-asserted Docket identities such as
`codex@docket.invalid`, not GitHub-linked user accounts. GitHub therefore lists
those commits as anonymous instead of creating contributor profile entries; this
section and the Git history are the attribution record.

## License

Docket is released under the [MIT License](LICENSE) — specification and
reference toolchain alike, so another implementation may quote `PROTOCOL.md`
and vendor `tools/` without restriction.
