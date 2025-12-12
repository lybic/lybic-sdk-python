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
import json
from io import BytesIO
from typing import Tuple, overload, TYPE_CHECKING

import httpx

from PIL import Image
from PIL.WebPImagePlugin import WebPImageFile

from lybic import dto

if TYPE_CHECKING:
    from lybic.lybic import LybicClient

class Sandbox:
    """
    Sandbox API
    """
    def __init__(self, client: "LybicClient"):
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
    async def create(self, data: dto.CreateSandboxDto) -> dto.Sandbox: ...

    @overload
    async def create(self, **kwargs) -> dto.Sandbox: ...

    async def create(self, *args, **kwargs) -> dto.Sandbox:
        """
        Create a new sandbox
        """
        if args and isinstance(args[0], dto.CreateSandboxDto):
            data = args[0]
        elif "data" in kwargs and isinstance(kwargs["data"], dto.CreateSandboxDto):
            data = kwargs["data"]
        else:
            data = dto.CreateSandboxDto(**kwargs)
        self.client.logger.debug(f"Creating sandbox with data: {data}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes", json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Create sandbox response: {response.text}")
        return dto.Sandbox.model_validate_json(response.text)

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
            json=data.model_dump(exclude_none=True))

    async def get_connection_details(self, sandbox_id: str)-> dto.ConnectDetails:
        """
        Get stream connection details for a sandbox
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

    async def get_shapes(self)-> dto.GetShapesResponseDto:
        """
        Get shapes of a sandbox
        :return:
        GetShapersResponseDto
        """
        self.client.logger.debug("Getting shapes")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/shapes"
        )
        self.client.logger.debug(f"Get shapes response: {response.text}")
        return dto.GetShapesResponseDto.model_validate_json(response.text)

    @overload
    async def execute_sandbox_action(self, sandbox_id: str, data: dto.ExecuteSandboxActionDto) -> dto.SandboxActionResponseDto: ...

    @overload
    async def execute_sandbox_action(self, sandbox_id: str, **kwargs) -> dto.SandboxActionResponseDto: ...

    async def execute_sandbox_action(self, sandbox_id: str, *args, **kwargs) -> dto.SandboxActionResponseDto:
        """
        Executes a computer use or mobile use action on the sandbox.
        The action can be either a computer use or mobile use action.
        """
        if args and isinstance(args[0], dto.ExecuteSandboxActionDto):
            data = args[0]
        elif "data" in kwargs:
            data_arg = kwargs["data"]
            if isinstance(data_arg, dto.ExecuteSandboxActionDto):
                data = data_arg
            elif isinstance(data_arg, dict):
                data = dto.ExecuteSandboxActionDto(**data_arg)
            else:
                raise TypeError(f"The 'data' argument must be of type {dto.ExecuteSandboxActionDto.__name__} or dict")
        else:
            data = dto.ExecuteSandboxActionDto(**kwargs)
        self.client.logger.debug(f"Execute sandbox action request: {data.model_dump_json(exclude_none=True)}")
        response = await self.client.request("POST",
                                             f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/execute",
                                             json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Execute sandbox action response: {response.text}")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    @overload
    async def copy_files(self, sandbox_id: str, data: dto.SandboxFileCopyRequestDto) -> dto.SandboxFileCopyResponseDto: ...

    @overload
    async def copy_files(self, sandbox_id: str, **kwargs) -> dto.SandboxFileCopyResponseDto: ...

    async def copy_files(self, sandbox_id: str, *args, **kwargs) -> dto.SandboxFileCopyResponseDto:
        """
        Copy files between sandbox and external locations (HTTP/S3).
        """
        if args and isinstance(args[0], dto.SandboxFileCopyRequestDto):
            data = args[0]
        elif "data" in kwargs:
            data_arg = kwargs["data"]
            if isinstance(data_arg, dto.SandboxFileCopyRequestDto):
                data = data_arg
            elif isinstance(data_arg, dict):
                data = dto.SandboxFileCopyRequestDto(**data_arg)
            else:
                raise TypeError(f"The 'data' argument must be of type {dto.SandboxFileCopyRequestDto.__name__} or dict")
        else:
            data = dto.SandboxFileCopyRequestDto(**kwargs)
        self.client.logger.debug(f"Copying files for sandbox {sandbox_id} with data {data.model_dump_json(exclude_none=True)}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/file/copy",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Copy files response: {response.text}")
        return dto.SandboxFileCopyResponseDto.model_validate_json(response.text)

    @overload
    async def execute_process(self, sandbox_id: str, data: dto.SandboxProcessRequestDto) -> dto.SandboxProcessResponseDto: ...

    @overload
    async def execute_process(self, sandbox_id: str, **kwargs) -> dto.SandboxProcessResponseDto: ...

    async def execute_process(self, sandbox_id: str, *args, **kwargs) -> dto.SandboxProcessResponseDto:
        """
        Execute a process inside sandbox.
        """
        if args and isinstance(args[0], dto.SandboxProcessRequestDto):
            data = args[0]
        elif "data" in kwargs:
            data_arg = kwargs["data"]
            if isinstance(data_arg, dto.SandboxProcessRequestDto):
                data = data_arg
            elif isinstance(data_arg, dict):
                data = dto.SandboxProcessRequestDto(**data_arg)
            else:
                raise TypeError(f"The 'data' argument must be of type {dto.SandboxProcessRequestDto.__name__} or dict")
        else:
            data = dto.SandboxProcessRequestDto(**kwargs)
        self.client.logger.debug(f"Executing process in sandbox {sandbox_id}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/process",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Execute process response: {response.text}")
        return dto.SandboxProcessResponseDto.model_validate_json(response.text)

    @overload
    async def create_from_image(self, data: dto.CreateSandboxFromImageDto) -> dto.CreateSandboxFromImageResponseDto: ...

    @overload
    async def create_from_image(self, **kwargs) -> dto.CreateSandboxFromImageResponseDto: ...

    async def create_from_image(self, *args, **kwargs) -> dto.CreateSandboxFromImageResponseDto:
        """
        Create a new sandbox from a machine image
        """
        if args and isinstance(args[0], dto.CreateSandboxFromImageDto):
            data = args[0]
        elif "data" in kwargs and isinstance(kwargs["data"], dto.CreateSandboxFromImageDto):
            data = kwargs["data"]
        else:
            data = dto.CreateSandboxFromImageDto(**kwargs)
        self.client.logger.debug(f"Creating sandbox from image with data: {data}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/from-image",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Create sandbox from image response: {response.text}")
        return dto.CreateSandboxFromImageResponseDto.model_validate_json(response.text)

    async def get_status(self, sandbox_id: str) -> dto.SandboxStatus:
        """
        Get the status of a sandbox (PENDING/RUNNING/STOPPED/ERROR)
        """
        self.client.logger.debug(f"Getting status for sandbox {sandbox_id}")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/status")
        self.client.logger.debug(f"Get sandbox status response: {response.text}")
        json_response = json.loads(response.text)
        return json_response['status']


    @overload
    async def create_machine_image(self, data: dto.CreateMachineImageDto) -> dto.MachineImageResponseDto: ...

    @overload
    async def create_machine_image(self, **kwargs) -> dto.MachineImageResponseDto: ...

    async def create_machine_image(self, *args, **kwargs) -> dto.MachineImageResponseDto:
        """
        Create a machine image from a sandbox
        """
        if args and isinstance(args[0], dto.CreateMachineImageDto):
            data = args[0]
        elif "data" in kwargs and isinstance(kwargs["data"], dto.CreateMachineImageDto):
            data = kwargs["data"]
        else:
            data = dto.CreateMachineImageDto(**kwargs)
        self.client.logger.debug(f"Creating machine image with data: {data}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/machine-images",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Create machine image response: {response.text}")
        return dto.MachineImageResponseDto.model_validate_json(response.text)

    async def list_machine_images(self) -> dto.MachineImagesResponseDto:
        """
        List all machine images
        """
        self.client.logger.debug("Listing machine images")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/machine-images")
        self.client.logger.debug(f"List machine images response: {response.text}")
        return dto.MachineImagesResponseDto.model_validate_json(response.text)

    async def delete_machine_image(self, image_id: str) -> None:
        """
        Delete a machine image
        """
        self.client.logger.debug(f"Deleting machine image {image_id}")
        await self.client.request(
            "DELETE",
            f"/api/orgs/{self.client.org_id}/machine-images/{image_id}")
