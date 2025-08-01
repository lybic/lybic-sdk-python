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
import httpx

from lybic import dto
from lybic.base import _LybicBaseClient


class LybicClient(_LybicBaseClient):
    """LybicAsyncClient is a client for all Lybic API."""

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
        super().__init__(
            org_id=org_id, api_key=api_key, endpoint=endpoint,
            timeout=timeout, extra_headers=extra_headers
        )

        self.client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Make a request to Lybic Restful API

        :param method:
        :param path:
        :param kwargs:
        :return:
        """
        url = f"{self.endpoint}{path}"
        headers = self.headers.copy()
        if method.upper() != "POST":
            headers.pop("Content-Type", None)

        response = await self.client.request(method, url, headers=headers, **kwargs)
        response.raise_for_status()
        return response

class Stats:
    """Stats are used for check"""
    def __init__(self, client: LybicClient):
        self.client = client

    async def get(self) -> dto.StatsResponseDto:
        """
        Get the stats of the organization, such as number of members, computers, etc.
        """
        self.client.logger.debug("Get stats requests")
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/stats")
        self.client.logger.debug("Get stats response: %s", response.text)
        return dto.StatsResponseDto.model_validate_json(response.text)
