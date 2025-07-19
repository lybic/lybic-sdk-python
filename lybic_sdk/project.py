
from lybic_sdk.lybic import LybicClient
from lybic_sdk import dto


class Project:
    """
    Projects class are used to organize Projects.
    """
    def __init__(self, client: LybicClient):
        self.client = client

    def list(self) -> dto.ListProjectsResponseDto:
        """
        List all projects in the organization.
        """
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/projects")
        return dto.ListProjectsResponseDto.model_validate_json(response.text)

    def create(self, data: dto.CreateProjectDto) -> dto.SingleProjectResponseDto:
        """
        Create a new project.
        """
        response = self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/projects", json=data.model_dump())
        return dto.SingleProjectResponseDto.model_validate_json(response.text)

    def delete(self, project_id: str) -> None:
        """
        Delete a project.
        """
        self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/projects/{project_id}")
