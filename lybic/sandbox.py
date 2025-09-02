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

# pylint: disable=fixme

"""sandbox.py provides the Sandbox API"""
import base64
from io import BytesIO
from typing import Tuple, overload

import httpx

from PIL import Image
from PIL.WebPImagePlugin import WebPImageFile

from lybic import dto
from lybic._api import deprecated
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
        self.client.logger.debug("Listing sandboxes requests")
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/sandboxes")
        self.client.logger.debug(f"Listing sandboxes response: {response.text}")
        return dto.SandboxListResponseDto.model_validate_json(response.text)

    @overload
    async def create(self, data: dto.CreateSandboxDto) -> dto.GetSandboxResponseDto: ...

    @overload
    async def create(self, **kwargs) -> dto.GetSandboxResponseDto: ...

    async def create(self, *args, **kwargs) -> dto.GetSandboxResponseDto:
        """
        Create a new sandbox
        """
        if args and isinstance(args[0], dto.CreateSandboxDto):
            data = args[0]
        else:
            data = dto.CreateSandboxDto(**kwargs)
        self.client.logger.debug(f"Creating sandbox with data: {data}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes", json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Create sandbox response: {response.text}")
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    async def get(self, sandbox_id: str) -> dto.GetSandboxResponseDto:
        """
        Get a sandbox
        """
        self.client.logger.debug(f"Get sandbox {sandbox_id}")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
        self.client.logger.debug(f"Get sandbox response: {response.text}")
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    async def delete(self, sandbox_id: str) -> None:
        """
        Delete a sandbox
        """
        self.client.logger.debug(f"Delete sandbox {sandbox_id}")
        await self.client.request(
            "DELETE",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Lybic Sandbox will support multiple types of tools in the future and will no longer be limited to computer_use. "
                "To execute a single action tool, such as computer_use, use the action execution method "
                "in the ComputerUse class. If no distinction is made, use the `execute_action` method in "
                "the Sandbox class."
    )
    @overload
    async def execute_computer_use_action(self, sandbox_id: str, data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto: ...
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Lybic Sandbox will support multiple types of tools in the future and will no longer be limited to computer_use. "
                "To execute a single action tool, such as computer_use, use the action execution method "
                "in the ComputerUse class. If no distinction is made, use the `execute_action` method in "
                "the Sandbox class."
    )
    @overload
    async def execute_computer_use_action(self, sandbox_id: str, **kwargs) -> dto.SandboxActionResponseDto: ...
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Lybic Sandbox will support multiple types of tools in the future and will no longer be limited to computer_use. "
                "To execute a single action tool, such as computer_use, use the action execution method "
                "in the ComputerUse class. If no distinction is made, use the `execute_action` method in "
                "the Sandbox class."
    )
    async def execute_computer_use_action(self, sandbox_id: str, *args, **kwargs) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as mcp.ComputerUse.execute_computer_use_action
        """
        if args and isinstance(args[0], dto.ComputerUseActionDto):
            data = args[0]
        elif "data" in kwargs:
            data_arg = kwargs["data"]
            if isinstance(data_arg, dto.ComputerUseActionDto):
                data = data_arg
            elif isinstance(data_arg, dict):
                data = dto.ComputerUseActionDto(**data_arg)
            else:
                raise TypeError(f"The 'data' argument must be of type {dto.ComputerUseActionDto.__name__} or dict")
        else:
            data = dto.ComputerUseActionDto(**kwargs)
        self.client.logger.debug(f"Execute computer use action request: {data.model_dump_json()}")
        response = await self.client.request("POST",
                                       f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
                                       json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Execute computer use action response: {response.text}")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    async def preview(self, sandbox_id: str) -> dto.SandboxActionResponseDto:
        """
        Preview a sandbox
        """
        self.client.logger.debug(f"Previewing sandbox {sandbox_id}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/preview")
        self.client.logger.debug(f"Previewed sandbox {sandbox_id}")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    async def extend_life(self, sandbox_id: str, seconds: int = 3600) -> None:
        """Extend the life of a sandbox.

        Args:
            sandbox_id: The ID of the sandbox to extend.
            seconds: The duration in seconds to extend the sandbox's life.
                     Default is 3600 (1 hour), max is 86400 (1 day).
                     The new max life time of the sandbox (relative to the current time) in seconds. Should not less
                     than 30 seconds or more than 24 hours. Note that the total maximum lifetime of a sandbox should
                     not longer than 13 days.
        """
        self.client.logger.debug(f"Extending life of sandbox {sandbox_id}")
        data = dto.ExtendSandboxDto(maxLifeSeconds=seconds)
        await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/extend",
            json=data.model_dump())

    async def get_connection_details(self, sandbox_id: str)-> dto.ConnectDetails:
        """
        Get connection details for a sandbox
        """
        sandbox = await self.get(sandbox_id)
        return sandbox.connectDetails

    async def get_screenshot(self, sandbox_id: str) -> Tuple[str, Image.Image, str]:
        """
        Get screenshot of a sandbox

        Return screenShot_url, screenshot_image, base64_str(utf-8 encode)
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

    # todo: 2025-09-02 a method called "execute_action" for computer-use, mobile-use and other sandbox tools.
