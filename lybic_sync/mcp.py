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

"""mcp.py: Synchronous MCP client for lybic MCP(Model Context Protocol) and Restful Interface API."""
from typing import overload, TYPE_CHECKING

from lybic import dto

if TYPE_CHECKING:
    from lybic_sync.lybic_sync import LybicSyncClient

# pylint: disable=invalid-name
class McpSync:
    """McpSync is a synchronous client for lybic MCP(Model Context Protocol) and Restful Interface API."""
    def __init__(self, client: "LybicSyncClient"):
        """
        Init MCP client with lybic client

        :param client: LybicSyncClient
        """
        self.client = client

    def list(self) -> dto.ListMcpServerResponse:
        """
        List all MCP servers in the organization

        :return:
        """
        self.client.logger.debug("List MCP servers request")
        response = self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers")
        self.client.logger.debug(f"List MCP servers response: {response.text}")
        return dto.ListMcpServerResponse.model_validate_json(response.text)

    @overload
    def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto: ...

    @overload
    def create(self, **kwargs) -> dto.McpServerResponseDto: ...

    def create(self, *args, **kwargs) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        if args and isinstance(args[0], dto.CreateMcpServerDto):
            data = args[0]
        elif "data" in kwargs and isinstance(kwargs["data"], dto.CreateMcpServerDto):
            data = kwargs["data"]
        else:
            data = dto.CreateMcpServerDto(**kwargs)
        self.client.logger.debug(f"Create MCP server request: {data.model_dump_json(exclude_none=True)}")
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Create MCP server response: {response.text}")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        self.client.logger.debug("Get default MCP server request")
        response = self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers/default")
        self.client.logger.debug(f"Get default MCP server response: {response.text}")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        self.client.logger.debug(f"Delete MCP server request: {mcp_server_id}")
        self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}")

    def set_sandbox(self, mcp_server_id: str, sandbox_id: str) -> None:
        """
        Set MCP server to a specific sandbox

        :param mcp_server_id: The ID of the MCP server
        :param sandbox_id: The ID of the sandbox to connect the MCP server to
        :return: None
        """
        data = dto.SetMcpServerToSandboxResponseDto(sandboxId=sandbox_id)
        self.client.logger.debug(f"Set MCP server to sandbox request: {data.model_dump_json(exclude_none=True)}")
        self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}/sandbox",
            json=data.model_dump(exclude_none=True))
