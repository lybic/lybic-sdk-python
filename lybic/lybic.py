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

import requests

from lybic import dto

class LybicClient:
    """LybicClient is a client for all Lybic API."""

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
        headers = self.headers.copy()
        if method != "POST":
            headers.pop("Content-Type", None)
        response = requests.request(method, url, headers=headers,timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response

    def make_mcp_endpoint(self, mcp_server_id: str) -> str:
        """
        Make MCP endpoint for a MCP server

        :param mcp_server_id:
        :return:
        """
        return f"{self.endpoint}/mcp/{mcp_server_id}"

class Stats:
    """Stats are used for check"""
    def __init__(self, client: LybicClient):
        self.client = client

    def get(self) -> dto.StatsResponseDto:
        """
        Get the stats of the organization, such as number of members, computers, etc.
        """
        response = self.client.request("GET", f"/api/orgs/{self.client.org_id}/stats")
        return dto.StatsResponseDto.model_validate_json(response.text)
