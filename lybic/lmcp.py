# lmcp.py: MCP client for lybic MCP(Model Context Protocol) and Restful Interface API.
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

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
        response = self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers")
        return dto.ListMcpServerResponse.model_validate_json(response.text)

    def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/mcp-servers",
            json=data.model_dump())
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        response = self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/mcp-servers/default")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}")

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


class ComputerUse:
    """ComputerUse is a client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client
        self.mcp = client.mcp

    def parse_model_output(self, data: dto.ComputerUseParseRequestDto) -> dto.ComputerUseActionResponseDto:
        """
        parse doubao-ui-tars output

        :param data:
        :return:
        """
        response = self.client.request(
            "POST",
            "/api/computer-use/parse",
            json=data.model_dump())
        return dto.ComputerUseActionResponseDto.model_validate_json(response.text)

    def execute_computer_use_action(self, sandbox_id: str,
                                    data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as sandbox.Sandbox.execute_computer_use_action
        """
        response = self.client.request("POST",
                                       f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
                                       json=data.model_dump())
        return dto.SandboxActionResponseDto.model_validate_json(response.text)
