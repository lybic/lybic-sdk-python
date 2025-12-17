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

"""base.py holds the base client for synchronous Lybic API."""
import logging
from typing import Optional

from lybic.authentication import LybicAuth

class _LybicSyncBaseClient:
    """_LybicSyncBaseClient is a base client for synchronous Lybic API."""

    def __init__(self,
                 auth: Optional[LybicAuth] = None,
                 timeout: int = 10,
                 max_retries: int = 3,
                 ):
        """
        Init lybic sync client with org_id, api_key and endpoint

        :param auth: LybicAuth instance
        :param org_id:
        :param api_key:
        :param endpoint:
        :param timeout:
        :param extra_headers:
        :param max_retries:
        """
        # Reuse the base client initialization from lybic.base
        # pylint: disable=import-outside-toplevel
        from lybic.base import _LybicBaseClient
        base_client = _LybicBaseClient(
            auth=auth,
            timeout=timeout,
            max_retries=max_retries
        )

        self.auth = base_client.auth
        self.timeout = base_client.timeout
        self.max_retries = base_client.max_retries
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
        return f"{self.endpoint}/api/mcp/{mcp_server_id}"
