# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
# Copyright (c) 2025        Lu Yicheng <luyicheng@tingyutech.com>
#
# Author: AEnjoy <aenjoyable@163.com>
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

"""sandbox.py provides the Sandbox API"""
import asyncio
from PIL import Image

from lybic import dto
from lybic.lybic import LybicClient

class Sandbox:
    """
    Sandbox API
    """
    def __init__(self, client: LybicClient):
        self.client = client

    def list(self) -> dto.SandboxListResponseDto:
        """
        List all sandboxes
        """
        return asyncio.run(self.client.get_async_client().sandbox.list())

    def create(self, data: dto.CreateSandboxDto) -> dto.GetSandboxResponseDto:
        """
        Create a new sandbox
        """
        return asyncio.run(self.client.get_async_client().sandbox.create(data))

    def get(self, sandbox_id: str) -> dto.GetSandboxResponseDto:
        """
        Get a sandbox
        """
        return asyncio.run(self.client.get_async_client().sandbox.get(sandbox_id))

    def delete(self, sandbox_id: str) -> None:
        """
        Delete a sandbox
        """
        return asyncio.run(self.client.get_async_client().sandbox.delete(sandbox_id))

    def execute_computer_use_action(self, sandbox_id: str, data: dto.ComputerUseActionDto) \
            -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as mcp.ComputerUse.execute_computer_use_action
        """
        return asyncio.run(self.client.get_async_client().sandbox.execute_computer_use_action(sandbox_id, data))

    def preview(self, sandbox_id: str) -> dto.SandboxActionResponseDto:
        """
        Preview a sandbox
        """
        return asyncio.run(self.client.get_async_client().sandbox.preview(sandbox_id))

    def get_connection_details(self, sandbox_id: str)-> dto.SandboxConnectionDetail:
        """
        Get connection details for a sandbox
        """
        return asyncio.run(self.client.get_async_client().sandbox.get_connection_details(sandbox_id))

    def get_screenshot(self, sandbox_id: str) -> (str, Image.Image, str):
        """
        Get screenshot of a sandbox

        Return screenShot_Url, screenshot_image, base64_str
        """
        return asyncio.run(self.client.get_async_client().sandbox.get_screenshot(sandbox_id))
