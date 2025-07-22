# sandbox.py provides the Sandbox API
import base64
from io import BytesIO

from PIL import Image
from PIL.WebPImagePlugin import WebPImageFile

from lybic import dto
from lybic.lybic import LybicClient

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

    def execute_computer_use_action(self, sandbox_id: str, data: dto.ComputerUseActionDto) \
            -> dto.SandboxActionResponseDto:
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

    def get_screenshot(self, sandbox_id: str) -> (str, Image.Image, str):
        """
        Get screenshot of a sandbox

        Return screenShot_Url, screenshot_image, base64_str
        """
        dto = self.preview(sandbox_id)
        screenshot_url = dto.screenShot

        screenshot_response = self.client.request("GET",screenshot_url)
        screenshot_response.raise_for_status()

        img = Image.open(BytesIO(screenshot_response.content))
        base64_str=''

        if isinstance(img, WebPImageFile):
            buffer = BytesIO()
            img.save(buffer, format="WebP")
            base64_str = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return  screenshot_url,img,base64_str
