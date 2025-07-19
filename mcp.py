import dto
from lybic import LybicClient


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
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/mcp-servers")
        return dto.ListMcpServerResponse.model_validate_json(response.text)

    def create(self, data: dto.CreateMcpServerDto) -> dto.McpServerResponseDto:
        """
        Create a mcp server

        :param data:
        :return:
        """
        response = self.client.request("POST", f"/api/orgs/{self.client.org_id}/mcp-servers", json=data.model_dump())
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def get_default(self) -> dto.McpServerResponseDto:
        """
        Get default mcp server

        :return:
        """
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/mcp-servers/default")
        return dto.McpServerResponseDto.model_validate_json(response.text)

    def delete(self, mcp_server_id: str) -> None:
        """
        Delete a mcp server

        :param mcp_server_id:
        :return:
        """
        self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/mcp-servers/{mcp_server_id}")


class ComputerUse:
    """ComputerUse is a client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client

    def parse_model_output(self, data: dto.ComputerUseParseRequestDto) -> dto.ComputerUseActionResponseDto:
        response = self.client.request("POST", "/api/computer-use/parse", json=data.model_dump())
        return dto.ComputerUseActionResponseDto.model_validate_json(response.text)