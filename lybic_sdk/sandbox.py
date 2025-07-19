# sandbox.py provides the Sandbox API
from lybic_sdk import dto
from lybic_sdk.lybic import LybicClient


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
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/sandboxes")
        return dto.SandboxListResponseDto.model_validate_json(response.text)

    def create(self, data: dto.CreateSandboxDto) -> dto.GetSandboxResponseDto:
        """
        Create a new sandbox
        """
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes", json=data.model_dump())
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    def get(self, sandbox_id: str) -> dto.GetSandboxResponseDto:
        """
        Get a sandbox
        """
        response = self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
        return dto.GetSandboxResponseDto.model_validate_json(response.text)

    def delete(self, sandbox_id: str) -> None:
        """
        Delete a sandbox
        """
        self.client.request(
            "DELETE",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")

    def execute_computer_use_action(self, sandbox_id: str, data: dto.ComputerUseActionDto) -> dto.SandboxActionResponseDto:
        """
        Execute a computer use action

        is same as mcp.ComputerUse.execute_computer_use_action
        """
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
            json=data.model_dump())
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    def preview(self, sandbox_id: str) -> dto.SandboxActionResponseDto:
        """
        Preview a sandbox
        """
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/preview")
        return dto.SandboxActionResponseDto.model_validate_json(response.text)

    def get_connection_details(self, sandbox_id: str)-> dto.SandboxConnectionDetail:
        """
        Get connection details for a sandbox
        """
        response =  self.client.request(
            "GET",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}")
        return dto.SandboxConnectionDetail.model_validate_json(response.text)
