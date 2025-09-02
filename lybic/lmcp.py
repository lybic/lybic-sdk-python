"""
lmcp.py has been moved to mcp.py

And it will be removed in the 1.0 stable version, please modify your import

from lybic.lmcp import MCP,ComputerUse
 ->
from lybic.mcp import MCP,ComputerUse

or

from lybic import MCP,ComputerUse
"""
# pylint: disable=unused-import

import warnings
from .mcp import MCP, ComputerUse

warnings.warn(
    "The 'lybic.lmcp' module has been moved to 'lybic.mcp' and is deprecated. It will be removed in version 1.0. Please update your imports.",
    DeprecationWarning,
    stacklevel=2
)
