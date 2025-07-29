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

"""lmcp.py: MCP client for lybic MCP(Model Context Protocol) and Restful Interface API."""
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CallToolResult

from lybic import dto
from lybic.lybic import LybicClient

class MCP:
    """AsyncMCP is a client for lybic MCP(Model Context Protocol) and Restful Interface API."""
    def __init__(self, client: LybicClient):
        """
        Init MCP client with lybic client

        :param client: LybicClient
        """
        self.client = client

    async def list(self) -> dto.ListMcpServerResponse:
        """
        List all MCP servers in the organization

        :return:
        """
        self.client.logger.debug("List MCP servers request")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers")
        self.client.logger.debug(f"List MCP servers response: {response.text}")
        return dto.ListMcpServerResponse.model_validate_json(response.text)

    async def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        self.client.logger.debug(f"Create MCP server request: {data.model_dump_json()}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers",
            json=data.model_dump())
        self.client.logger.debug(f"Create MCP server response: {response.text}")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    async def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        self.client.logger.debug("Get default MCP server request")
        response = await self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers/default")
        self.client.logger.debug(f"Get default MCP server response: {response.text}")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    async def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        self.client.logger.debug(f"Delete MCP server request: {mcp_server_id}")
        await self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}")

    async def set_sandbox(self, mcp_server_id: str, sandbox_id: str) -> None:
        """
        Set MCP server to a specific sandbox

        :param mcp_server_id: The ID of the MCP server
        :param sandbox_id: The ID of the sandbox to connect the MCP server to
        :return: None
        """
        data = dto.SetMcpServerToSandboxResponseDto(sandboxId=sandbox_id)
        self.client.logger.debug(f"Set MCP server to sandbox request: {data.model_dump_json()}")
        await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}/sandbox",
            json=data.model_dump())

    async def call_tool_async(self,
                              mcp_server_id: str,
                              tool_name: str = "computer-use",
                              tool_args: dict = None)->CallToolResult:
        """
        Call a tool on mcp server

        :param mcp_server_id:
        :param tool_name:
        :param tool_args:
        :return:
        """
        self.client.logger.debug(f"Call tool request: {tool_name} with arguments: {tool_args}")
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
                    result = await session.call_tool(tool_name, tool_args)
                    self.client.logger.debug(f"Call tool response: {result.model_dump_json()}")
                    return result

        except Exception as e:
            raise RuntimeError(f"Failed to call tool: {e}") from e

class ComputerUse:
    """AsyncComputerUse is a client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client

    async def parse_model_output(self, data: dto.ComputerUseParseRequestDto) -> dto.ComputerUseActionResponseDto:
        """
        parse doubao-ui-tars output

        :param data:
        :return:
        """
        self.client.logger.debug(f"Parse model output request: {data.model_dump_json()}")
        response = await self.client.request(
            "POST",
            "/api/computer-use/parse",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return dto.ComputerUseActionResponseDto.model_validate_json(response.text)

    async def execute_computer_use_action(self, sandbox_id: str,
                                    data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as sandbox.Sandbox.execute_computer_use_action
        """
        self.client.logger.debug(f"Execute computer use action request: {data.model_dump_json()}")
        response = await self.client.request("POST",
                                       f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
                                       json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Execute computer use action response: {response.text}")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)
