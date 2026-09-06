# Docket
<!-- mcp-name: io.github.metet/docket -->

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

Docket has **zero runtime dependencies** — it relies solely on Python's standard library and Git.

- **Python:** 3.8 or newer.
- **Git:** Any modern Git supporting `core.hooksPath`.
- **Packaged launcher:** [`uv`](https://docs.astral.sh/uv/) provides `uvx` and
  installs Docket in an isolated environment.

The PyPI package and official MCP Registry entry are prepared in this repository
but have not been published yet. Until the human maintainer makes that release,
use the source-checkout instructions below; do not install an unrelated package
with the same name. Docket is continuously verified on Linux, macOS, and native
Windows with Python 3.8, 3.11, and 3.13.

### Two-Tier Tool Layout

Docket tools are organized into two groups:

1. **Shared Toolchain** (installed by `uvx`, or run from the Docket source clone):
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

After version 0.3.0 is published, the standard installation is one command:

```bash
uvx docket init /path/to/my-project
```

The native Windows PowerShell form is the same; quote paths containing spaces:

```powershell
uvx docket init "C:\path\to\my project"
```

For now, install from the public source checkout:

```bash
git clone https://github.com/metet/docket.git
python3 docket/tools/docket-init /path/to/my-project
```

On Windows PowerShell, use the Python launcher:

```powershell
git clone https://github.com/metet/docket.git
py -3 docket/tools/docket-init C:\path\to\my-project
```

The default copies the protocol and per-repository tools, so the initialized
project does not depend on the installer remaining present. `--link` is intended
for development from a persistent source checkout; do not use it with an
ephemeral `uvx` environment.

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

The initialized store name is always `docket/`. `docket-init --store` was removed
because a custom directory could bypass the installed Git hooks. Low-level
environment overrides remain for test fixtures and legacy workspace discovery,
but are not part of normal installation.

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
| **`tools/docket-test`** | Self-contained regression test suite (package, platform, and protocol behavior). |
| **`tools/docket-commit`** | Commit as a named party: sets the git author for that one invocation and records a `Docket-Party:` trailer. |
| **`tools/git-hooks/`** | Tracked git hooks. `pre-commit` runs the lint and the suite; `commit-msg` refuses a commit whose declared party contradicts the filings it carries. Opt in per clone with `git config core.hooksPath tools/git-hooks`. |

### Running the checks

```bash
python3 tools/docket-lint    # schema and state-machine legality
python3 tools/docket-test    # behavioural checks
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

`docket-mcp` allows MCP-enabled agents (Claude Code, Qwen Code, Cursor, Codex) to interact using structured tool calls rather than raw shell scripts.

After publication, install `io.github.metet/docket` from an MCP Registry-aware
client and set `DOCKET_PARTY` to that client's registered name. For clients that
take a command configuration directly, the portable standard is:

```json
{
  "command": "uvx",
  "args": ["docket"],
  "env": {"DOCKET_PARTY": "your-party-name"}
}
```

`uvx docket` starts the stdio server with no subcommand; `uvx docket mcp` and
`uvx --from docket docket-mcp` are equivalent explicit forms. Before the package
is published, replace that command with the source-checkout launcher shown below.

### Automatic Store Resolution

The MCP server first checks the current directory, then the enclosing Git root,
then a matching approved workspace in `~/.config/docket/workspaces`, and finally
roots supplied by the MCP client. This lets one installation serve many projects
without placing machine-specific paths in the package.

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

### Source-checkout registration examples

These are usable now and remain useful for Docket development. On native
Windows, use `py` as the command and put `-3` before the script path.

* **Claude Code:**
  ```bash
  claude mcp add docket -e DOCKET_PARTY=claude -- python3 /path/to/tools/docket-mcp
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
        "DOCKET_PARTY": "qwen"
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
