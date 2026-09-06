# Releasing Docket

Publishing changes public package state and requires the human maintainer's
PyPI and GitHub credentials. Agents may prepare and verify artifacts, but must
not run the upload or MCP Registry publication commands.

## Prepare and verify locally

1. Set `__version__` in `tools/docket_lib.py`, and set the same version in both
   locations in `server.json`.
2. Refresh the wheel's copies and verify there is no drift:

   ```bash
   python tools/docket-sync-package
   python tools/docket-sync-package --check
   ```

3. Run the source checks and build both distributions:

   ```bash
   python tools/docket-test
   python tools/docket-lint docket
   python -m build
   python tools/docket-package-test dist
   ```

The package README must retain the ownership token
`mcp-name: io.github.metet/docket`. The artifact test checks it in wheel
metadata, all eight console entry points, bundled scaffold assets, a fresh wheel
installation, stdio initialization, and nested Git-root store discovery.

## Human publication steps

From a clean, tagged commit whose artifacts passed the checks above:

```bash
python -m twine upload dist/*
mcp-publisher login github
mcp-publisher publish
```

Upload to PyPI before publishing `server.json`, because the Registry verifies
that the declared package and version exist and that its PyPI README claims
`io.github.metet/docket`. Confirm both public entries after publication. PyPI
project-name availability is not guaranteed until the first upload succeeds.
