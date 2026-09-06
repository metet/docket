"""Run the dependency-free tools bundled in the wheel.

The files under ``tools/`` remain the canonical source-checkout commands.  A
byte-for-byte copy is packaged so the PyPI and checkout entry points execute
the same implementation; ``tools/docket-sync-package --check`` prevents drift.
"""
from pathlib import Path
import re
import runpy
import sys


ASSET_ROOT = Path(__file__).resolve().parent / "assets"
TOOL_ROOT = ASSET_ROOT / "tools"


def package_version():
    text = (TOOL_ROOT / "docket_lib.py").read_text(encoding="utf-8")
    match = re.search(r'^__version__\s*=\s*["\']([^"\']+)["\']', text, re.MULTILINE)
    if not match:
        raise RuntimeError("bundled docket_lib.py has no __version__")
    return match.group(1)


def run_tool(name, argv=None):
    """Execute a bundled tool exactly as if its script had been invoked."""
    script = TOOL_ROOT / name
    if not script.is_file():
        raise RuntimeError("bundled Docket tool is missing: " + name)
    old_argv = sys.argv
    inserted = str(TOOL_ROOT)
    sys.path.insert(0, inserted)
    sys.argv = [name, *(old_argv[1:] if argv is None else argv)]
    try:
        runpy.run_path(str(script), run_name="__main__")
    finally:
        sys.argv = old_argv
        if sys.path and sys.path[0] == inserted:
            sys.path.pop(0)
    return 0
