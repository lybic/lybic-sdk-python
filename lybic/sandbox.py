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
import base64
from io import BytesIO
from typing import Tuple

import httpx

from PIL import Image
from PIL.WebPImagePlugin import WebPImageFile

from lybic import dto
from lybic.lybic import LybicClient

class Sandbox:
    """
    Sandbox API
    """
    def __init__(self, client: LybicClient):
        self.client = client

    async def list(self) -> dto.SandboxListResponseDto:
        """
        List all sandboxes
        """
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/sandboxes")
        return dto.SandboxListResponseDto.model_validate_json(response.text)

    async def create(self, data: dto.CreateSandboxDto) -> dto.GetSandboxResponseDto:
        """
        Create a new sandbox
        """
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes", json=data.model_dump(exclude_none=True))
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    async def get(self, sandbox_id: str) -> dto.GetSandboxResponseDto:
        """
        Get a sandbox
        """
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    async def delete(self, sandbox_id: str) -> None:
        """
        Delete a sandbox
        """
        await self.client.request(
            "DELETE",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")

    async def execute_computer_use_action(self, sandbox_id: str, data: dto.ComputerUseActionDto) \
            -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as mcp.ComputerUse.execute_computer_use_action
        """
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
            json=data.model_dump())
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    async def preview(self, sandbox_id: str) -> dto.SandboxActionResponseDto:
        """
        Preview a sandbox
        """
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/preview")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    async def get_connection_details(self, sandbox_id: str)-> dto.SandboxConnectionDetail:
        """
        Get connection details for a sandbox
        """
        response =  await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
        return dto.SandboxConnectionDetail.model_validate_json(response.text)

    async def get_screenshot(self, sandbox_id: str) -> Tuple[str, Image.Image, str]:
        """
        Get screenshot of a sandbox

        Return screenShot_Url, screenshot_image, base64_str
        """
        result = await self.preview(sandbox_id)
        screenshot_url = result.screenShot

        async with httpx.AsyncClient() as client:
            screenshot_response = await client.get(
                screenshot_url,
                timeout=self.client.timeout
            )
            screenshot_response.raise_for_status()

            img = Image.open(BytesIO(screenshot_response.content))
            base64_str=''

            if isinstance(img, WebPImageFile):
                buffer = BytesIO()
                img.save(buffer, format="WebP")
                base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return screenshot_url,img,base64_str


    async def get_screenshot_base64(self, sandbox_id: str) -> str:
        """
        Get screenshot of a sandbox in base64 format
        """
        _, _, base64_str = await self.get_screenshot(sandbox_id)
        return base64_str
