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
import asyncio

from lybic import dto
from lybic.lybic import LybicClient

class MCP:
    """MCP is a client for lybic MCP(Model Context Protocol) and Restful Interface API."""
    def __init__(self, client: LybicClient):
        """
        Init MCP client with lybic client

        :param client: LybicClient
        """
        self.client = client

    def list(self) -> dto.ListMcpServerResponse:
        """
        List all MCP servers in the organization

        :return:
        """
        return asyncio.run(self.client.get_async_client().mcp.list())

    def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        return asyncio.run(self.client.get_async_client().mcp.create(data))

    def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        return asyncio.run(self.client.get_async_client().mcp.get_default())

    def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        return asyncio.run(self.client.get_async_client().mcp.delete(mcp_server_id))

    def set_sandbox(self, mcp_server_id: str, sandbox_id: str) -> None:
        """
        Set MCP server to a specific sandbox

        :param mcp_server_id: The ID of the MCP server
        :param sandbox_id: The ID of the sandbox to connect the MCP server to
        :return: None
        """
        data = dto.SetMcpServerToSandboxResponseDto(sandboxId=sandbox_id)
        return asyncio.run(self.client.get_async_client().mcp.set_sandbox(mcp_server_id, data))

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
        return self.client.get_async_client().mcp.call_tool_async(mcp_server_id, tool_name, tool_args)

class ComputerUse:
    """ComputerUse is a client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client

    def parse_model_output(self, data: dto.ComputerUseParseRequestDto) -> dto.ComputerUseActionResponseDto:
        """
        parse doubao-ui-tars output

        :param data:
        :return:
        """
        return asyncio.run(self.client.get_async_client().computer_use.parse_model_output(data))

    def execute_computer_use_action(self, sandbox_id: str,
                                    data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as sandbox.Sandbox.execute_computer_use_action
        """
        return asyncio.run(self.client.get_async_client().computer_use.execute_computer_use_action(sandbox_id, data))
