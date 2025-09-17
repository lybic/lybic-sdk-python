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

"""
In the OSWorld benchmark, in addition to common GUI keyboard and mouse operations, there are also several shortcut action spaces.
This expanded action space allows agents to perform more actions in smaller steps, enabling more functionality,
ultimately significantly improving the user experience.
This file adapts the action spaces of several well-known OSWorld agents to improve scalability and simplify developer
work in complex AI workflows.

Please view: https://github.com/xlang-ai/OSWorld/tree/main/mm_agents
"""
import sys
import time

from lybic.pyautogui import Pyautogui
from lybic.lybic import LybicClient


class OSWorld(Pyautogui):
    """
    OSWorld is a Python library for controlling the mouse and keyboard on Windows, macOS, and Linux.
    It provides a simple but effective way to automate tasks on these operating systems.
    """
    def __init__(self, client: LybicClient, sandbox_id: str):
        super().__init__(client, sandbox_id)
        self.platform: str = sys.platform.lower()

    def open(self,app_or_filename:str):
        """
        Opens an application or file.

        :param app_or_filename:
        :return:
        """
        if self.platform.startswith("darwin"):
            # macOS: Command+Space to open Spotlight
            self.hotkey("command", "space", interval=0.2)
            time.sleep(0.5)
            self.typewrite(app_or_filename)
            time.sleep(1.0)
            self.press("enter")
            time.sleep(0.5)
        elif self.platform.startswith("linux"):
            # Linux: Win key to open application menu
            self.press("super")
            time.sleep(0.5)
            self.typewrite(app_or_filename)
            time.sleep(1.0)
            self.press("enter")
            time.sleep(0.5)
        elif self.platform.startswith("win"):
            # Windows: Win+R to open Run dialog
            self.hotkey("win", "r", interval=0.1)
            time.sleep(0.5)
            self.typewrite(app_or_filename)
            time.sleep(1.0)
            self.press("enter")
            time.sleep(1.0)
        else:
            raise NotImplementedError(f"Open not supported on platform: {self.platform}")
