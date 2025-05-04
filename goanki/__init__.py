"""GoAnki package initializer."""

from __future__ import annotations

from importlib import resources

__all__ = ["__version__", "get_version"]

__version__ = "0.1.0"


def get_version() -> str:
    """Return the package version."""
    return __version__


def data_path(*parts: str) -> str:
    """
    Return an absolute path to a data resource bundled with the package.

    This helper allows other modules (for example config defaults) to access
    files stored inside the package without hardcoding relative paths.
    """
    return str(resources.files(__package__).joinpath(*parts))


