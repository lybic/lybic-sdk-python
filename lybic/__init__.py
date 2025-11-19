# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
#
# These Terms of Service ("Terms") set forth the rules governing your access to and use of the website lybic.ai
# ("Website"), our web applications, and other services (collectively, the "Services") provided by Beijing Tingyu
# Technology Co., Ltd. ("Company," "we," "us," or "our"), a company registered in Haidian District, Beijing. Any
# breach of these Terms may result in the suspension or termination of your access to the Services.
# By accessing and using the Services and/or the Website, you represent that you are at least 18 years old,
# acknowledge that you have read and understood these Terms, and agree to be bound by them. By using or accessing
# the Services and/or the Website, you further represent and warrant that you have the legal capacity and authority
# to agree to these Terms, whether as an individual or on behalf of a company. If you do not agree to all of these
# Terms, do not access or use the Website or Services.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

""" Lybic SDK import header"""

__version__ = "0.11.0" # SDK Api Leval

# Strategy for handling extra fields in the lybic api response
# "ignore" means ignore extra fields, which will ensure that your SDK version remains compatible with the Lybic platform,
# but it may cause compatibility issues with future versions of the SDK.
# "forbid" means that the SDK will throw an error if it encounters extra fields in the response, which will force you to
# update your SDK when the Lybic platform is updated, and may have a certain impact on your online environment.
from .dto import json_extra_fields_policy

# Lybic Client
from .authentication import LybicAuth
from .lybic import LybicClient

# Exceptions
from .exceptions import LybicError, LybicAPIError, LybicInternalError

# MCP Operations
from .mcp import MCP, Mcp

#  Tools
from .tools import ComputerUse

# Project
from .project import Project

# Pyautogui
from .pyautogui import Pyautogui

# Sandbox
from .sandbox import Sandbox

# Stats
from .stats import Stats

__all__ = [
    "__version__",
    "LybicAuth",
    "LybicClient",

    "LybicError",
    "LybicAPIError",
    "LybicInternalError",

    "MCP",
    "ComputerUse",
    "Project",
    "Pyautogui",
    "Sandbox",
    "Stats",

    "json_extra_fields_policy",
]

def __dir__() -> list[str]:
    return list(__all__)
