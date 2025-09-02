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

import sys
from .mcp import MCP,ComputerUse

print("lmcp.py has been moved to mcp.py",file=sys.stderr)
