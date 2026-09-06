"""Unified ``docket`` command; no arguments starts the stdio MCP server."""
import sys

from ._runner import run_tool


COMMANDS = {
    "mcp": "docket-mcp",
    "init": "docket-init",
    "workspace": "docket-workspace",
    "lint": "docket-lint",
    "new": "docket-new",
    "index": "docket-index",
    "commit": "docket-commit",
}


def usage():
    return """usage: docket [COMMAND] [ARGS...]

With no COMMAND, run the Docket MCP server over stdio.

commands:
  mcp        run the MCP server explicitly
  init       scaffold Docket in a repository
  workspace  manage trusted workspaces
  lint       validate a Docket store
  new        create a filing
  index      regenerate INDEX.md
  commit     commit with Docket party attribution
"""


def main():
    args = sys.argv[1:]
    if not args:
        return run_tool("docket-mcp", [])
    if args[0] in ("-h", "--help", "help"):
        print(usage(), end="")
        return 0
    tool = COMMANDS.get(args[0])
    if tool is None:
        print("docket: unknown command: " + args[0], file=sys.stderr)
        print(usage(), file=sys.stderr, end="")
        return 2
    return run_tool(tool, args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
