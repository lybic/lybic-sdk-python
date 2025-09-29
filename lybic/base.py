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

"""base.py holds the base client for Lybic API."""
import logging
import os
import warnings
from sys import stderr
from typing import Optional

from lybic.authentication import LybicAuth

_sentinel = object()

class _LybicBaseClient:
    """_LybicBaseClient is a base client for all Lybic API."""

    def __init__(self,
                 auth: Optional[LybicAuth] = None,
                 org_id: str = _sentinel,
                 api_key: str = _sentinel,
                 endpoint: str = _sentinel,
                 timeout: int = 10,
                 extra_headers: dict = _sentinel,
                 max_retries: int = 3,
                 ):
        """
        Init lybic client with org_id, api_key and endpoint

        :param auth: LybicAuth instance
        :param org_id:
        :param api_key:
        :param endpoint:
        """
        if auth:
            self.auth = auth
        else:
            user_provided_auth_params = any(
                val is not _sentinel for val in (org_id, api_key, endpoint, extra_headers)
            )
            if user_provided_auth_params:
                warnings.warn(
                    "Passing `org_id`, `api_key`, `endpoint`, or `extra_headers` to the client constructor is deprecated "
                    "and will be removed in v1.0.0. Please use `LybicClient(auth=LybicAuth(...))` instead.",
                    stacklevel=3
                )

            if org_id is _sentinel:
                org_id = os.getenv("LYBIC_ORG_ID")
            if api_key is _sentinel:
                api_key = os.getenv("LYBIC_API_KEY")
            if endpoint is _sentinel:
                endpoint = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.cn")
            if extra_headers is _sentinel:
                extra_headers = None
            assert org_id, "LYBIC_ORG_ID is required"
            assert endpoint, "LYBIC_API_ENDPOINT is required"

            self.auth = LybicAuth(
                org_id=org_id,
                api_key=api_key,
                endpoint=endpoint,
                extra_headers=extra_headers
            )

        if timeout < 0:
            print("Warning: Timeout cannot be negative, set to 10", file=stderr)
            timeout = 10
        self.timeout = timeout
        self.max_retries = max(max_retries, 0)

        self.logger = logging.getLogger(__name__)

    @property
    def headers(self):
        """
        Get headers for requests

        :return:
        """
        return self.auth.headers

    @property
    def endpoint(self):
        """
        Get endpoint for requests

        :return:
        """
        return self.auth.endpoint

    @property
    def org_id(self):
        """
        Get org_id for requests

        :return:
        """
        return self.auth.org_id

    @property
    def _api_key(self):
        return self.auth.api_key

    def make_mcp_endpoint(self, mcp_server_id: str) -> str:
        """
        Make MCP endpoint for a MCP server

        :param mcp_server_id:
        :return:
        """
        return f"{self.endpoint}/mcp/{mcp_server_id}"
