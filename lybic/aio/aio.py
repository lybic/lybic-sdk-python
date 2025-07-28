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

"""lybic.py is the main entry point for Lybic API."""

import os
from sys import stderr
import base64
from io import BytesIO

import httpx
from PIL import Image
from PIL.WebPImagePlugin import WebPImageFile
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

from lybic import dto

class LybicAsyncClient:
    """LybicAsyncClient is a client for all Lybic API."""

    def __init__(self,
                 org_id: str = os.getenv("LYBIC_ORG_ID"),
                 api_key: str = os.getenv("LYBIC_API_KEY"),
                 endpoint: str = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.cn"),
                 timeout: int = 10,
                 extra_headers: dict = None
                 ):
        """
        Init lybic client with org_id, api_key and endpoint

        :param org_id:
        :param api_key:
        :param endpoint:
        """
        assert org_id, "LYBIC_ORG_ID is required"
        assert endpoint, "LYBIC_API_ENDPOINT is required"

        self.headers = {}
        if extra_headers:
            self.headers.update(extra_headers)

        # if x-trial-session-token is provided, use it instead of api_key
        if not (extra_headers and 'x-trial-session-token' in extra_headers):
            assert api_key, "LYBIC_API_KEY is required when x-trial-session-token is not provided"
            self.headers["x-api-key"] = api_key

        if endpoint.endswith("/"):
            self.endpoint = endpoint[:-1]

        if timeout < 0:
            print("Warning: Timeout cannot be negative, set to 10",file=stderr)
            timeout = 10
        
        self.timeout = timeout
        self.org_id = org_id
        self.endpoint = endpoint

        self.headers["Content-Type"]= "application/json"
        
        self.client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        self.stats = AsyncStats(self)
        self.mcp = AsyncMCP(self)
        self.computer_use = AsyncComputerUse(self)
        self.project = AsyncProject(self)
        self.sandbox = AsyncSandbox(self)

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Make a request to Lybic Restful API

        :param method:
        :param path:
        :param kwargs:
        :return:
        """
        url = f"{self.endpoint}{path}"
        headers = self.headers.copy()
        if method.upper() != "POST":
            headers.pop("Content-Type", None)
        
        response = await self.client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response

    def make_mcp_endpoint(self, mcp_server_id: str) -> str:
        """
        Make MCP endpoint for a MCP server

        :param mcp_server_id:
        :return:
        """
        return f"{self.endpoint}/mcp/{mcp_server_id}"

class AsyncStats:
    """Stats are used for check"""
    def __init__(self, client: LybicAsyncClient):
        self.client = client

    async def get(self) -> dto.StatsResponseDto:
        """
        Get the stats of the organization, such as number of members, computers, etc.
        """
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/stats")
        return dto.StatsResponseDto.model_validate_json(response.text)

class AsyncMCP:
    """AsyncMCP is a client for lybic MCP(Model Context Protocol) and Restful Interface API."""
    def __init__(self, client: "LybicAsyncClient"):
        """
        Init MCP client with lybic client

        :param client: LybicAsyncClient
        """
        self.client = client

    async def list(self) -> dto.ListMcpServerResponse:
        """
        List all MCP servers in the organization

        :return:
        """
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers")
        return dto.ListMcpServerResponse.model_validate_json(response.text)

    async def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers",
            json=data.model_dump())
        return dto.McpServerResponseDto.model_validate_json(response.text)

    async def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers/default")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    async def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        await self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}")

    async def set_sandbox(self, mcp_server_id: str, sandbox_id: str) -> None:
        """
        Set MCP server to a specific sandbox

        :param mcp_server_id: The ID of the MCP server
        :param sandbox_id: The ID of the sandbox to connect the MCP server to
        :return: None
        """
        data = dto.SetMcpServerToSandboxResponseDto(sandboxId=sandbox_id)
        await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}/sandbox",
            json=data.model_dump())

    async def call_tool_async(self,
                              mcp_server_id: str,
                              tool_name: str = "computer-use",
                              tool_args: dict = None):
        """
        Call a tool on mcp server

        :param mcp_server_id:
        :param tool_name:
        :param tool_args:
        :return:
        """
        try:
            async with streamablehttp_client(self.client.make_mcp_endpoint(mcp_server_id),
                                             headers=self.client.headers,
                                             timeout=30
            ) as (
                    read_stream,
                    write_stream,
                    _,
            ):
                async with ClientSession(read_stream, write_stream) as session:
                    await session.initialize()
                    return await session.call_tool(tool_name, tool_args)
        except Exception as e:
            raise RuntimeError(f"Failed to call tool: {e}") from e


class AsyncComputerUse:
    """AsyncComputerUse is a client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: "LybicAsyncClient"):
        self.client = client

    async def parse_model_output(self, data: dto.ComputerUseParseRequestDto) -> dto.ComputerUseActionResponseDto:
        """
        parse doubao-ui-tars output

        :param data:
        :return:
        """
        response = await self.client.request(
            "POST",
            "/api/computer-use/parse",
            json=data.model_dump(exclude_none=True))
        return dto.ComputerUseActionResponseDto.model_validate_json(response.text)

    async def execute_computer_use_action(self, sandbox_id: str,
                                    data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as sandbox.Sandbox.execute_computer_use_action
        """
        response = await self.client.request("POST",
                                       f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
                                       json=data.model_dump(exclude_none=True))
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

class AsyncProject:
    """
    AsyncProjects class are used to organize Projects.
    """
    def __init__(self, client: LybicAsyncClient):
        self.client = client

    async def list(self) -> dto.ListProjectsResponseDto:
        """
        List all projects in the organization.
        """
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/projects")
        return dto.ListProjectsResponseDto.model_validate_json(response.text)

    async def create(self, data: dto.CreateProjectDto) -> dto.SingleProjectResponseDto:
        """
        Create a new project.
        """
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/projects", json=data.model_dump())
        return dto.SingleProjectResponseDto.model_validate_json(response.text)

    async def delete(self, project_id: str) -> None:
        """
        Delete a project.
        """
        await self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/projects/{project_id}")

class AsyncSandbox:
    """
    Sandbox API
    """
    def __init__(self, client: LybicAsyncClient):
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

    async def get_screenshot(self, sandbox_id: str) -> (str, Image.Image, str):
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

        return  screenshot_url,img,base64_str


    async def get_screenshot_base64(self, sandbox_id: str) -> str:
        """
        Get screenshot of a sandbox in base64 format
        """
        _, _, base64_str = await self.get_screenshot(sandbox_id)
        return base64_str
