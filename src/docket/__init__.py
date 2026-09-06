"""Docket's packaged command-line and MCP entry points."""
from ._runner import package_version

__version__ = package_version()

__all__ = ["__version__"]
