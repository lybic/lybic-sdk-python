import os
import requests

import dto

from mcp import MCP, ComputerUse
from project import Project
from sandbox import Sandbox


class LybicClient:
    """LybicClient is a client for all Lybic API."""

    def __init__(self,
                 org_id: str = os.getenv("LYBIC_ORG_ID"),
                 api_key: str = os.getenv("LYBIC_API_KEY"),
                 endpoint: str = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.com/v1")):
        """
        Init lybic client with org_id, api_key and endpoint

        :param org_id:
        :param api_key:
        :param endpoint:
        """
        assert org_id, "LYBIC_ORG_ID is required"
        assert api_key, "LYBIC_API_KEY is required"
        assert endpoint, "LYBIC_API_ENDPOINT is required"

        self.org_id = org_id
        self.endpoint = endpoint
        self.headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

        self.mcp = MCP(self)
        self.sandboxes = Sandbox(self)
        self.projects = Project(self)
        self.computer_use = ComputerUse(self)
        self.stats = Stats(self)

        # Auth Test
        self.stats.get()

    def request(self, method: str, path: str, **kwargs) -> requests.Response:
        """
        Make a request to Lybic Restful API

        :param method:
        :param path:
        :param kwargs:
        :return:
        """
        url = f"{self.endpoint}{path}"
        headers = self.headers
        if method != "POST":
            headers.pop("Content-Type")
        response = requests.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response


class Stats:
    """Stats are used for check"""
    def __init__(self, client: LybicClient):
        self.client = client

    def get(self) -> dto.StatsResponseDto:
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/stats")
        return dto.StatsResponseDto.model_validate_json(response.text)
