"""Helper functions for managing the Lybic API.

This module is only relevant for Lybic developers, not for users.

.. warning::

    This module and its submodules are for internal use only.  Do not use them
    in your own code.  We may change the API at any time with no warning.

"""

__all__ = [
    "deprecated",
    "LybicDeprecationWarning",
    "LybicPendingDeprecationWarning",
    "warn_deprecated",
    "rename_parameter",
]

from .deprecation import (
    deprecated,
    LybicDeprecationWarning,
    LybicPendingDeprecationWarning,
    warn_deprecated,
    rename_parameter
)

def __dir__() -> list[str]:
    return list(__all__)
