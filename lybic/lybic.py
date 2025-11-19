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
import asyncio
import json
from typing import Optional
import httpx

from lybic.authentication import LybicAuth
from lybic.base import _LybicBaseClient, _sentinel
from lybic.exceptions import LybicAPIError, LybicInternalError


class LybicClient(_LybicBaseClient):
    """LybicAsyncClient is a client for all Lybic API."""

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

        :param auth:
        :param org_id:
        :param api_key:
        :param endpoint:
        :param max_retries: maximum number of retries for failed requests
        """
        super().__init__(
            auth=auth, org_id=org_id, api_key=api_key, endpoint=endpoint,
            timeout=timeout, extra_headers=extra_headers, max_retries=max_retries
        )

        self.client: httpx.AsyncClient | None = None
        self._in_context = False

    def _ensure_client_is_open(self):
        if self.client is None:
            self.client = httpx.AsyncClient(headers=self.headers, timeout=self.timeout)
        elif self.client.is_closed:
            raise RuntimeError("The client has been closed and cannot be reused. Please create a new client instance.")

    async def __aenter__(self):
        if self._in_context:
            raise RuntimeError("Cannot re-enter context.")
        if self.client and not self.client.is_closed:
            raise RuntimeError("Cannot enter context with an already-active client.")

        self._in_context = True
        self._ensure_client_is_open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._in_context = False
        await self.close()

    async def close(self):
        """Close the underlying httpx.AsyncClient."""
        if self._in_context:
            return
        if self.client:
            await self.client.aclose()

    async def request(self, method: str, path: str, **kwargs) -> httpx.Response:
        """
        Make a request to Lybic Restful API

        :param method:
        :param path:
        :param kwargs:
        :return:
        :raises LybicAPIError: When API returns structured error response
        :raises LybicInternalError: When 5xx error occurs from reverse proxy
        :raises httpx.RequestError: When network-level error occurs
        """
        self._ensure_client_is_open()

        url = f"{self.endpoint}{path}"
        headers = self.headers.copy()
        if method.upper() != "POST":
            headers.pop("Content-Type", None)

        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self.client.request(method, url, headers=headers, **kwargs)
                response.raise_for_status()
                return response
            except httpx.HTTPStatusError as e:
                # Check if this is the last attempt
                if attempt < self.max_retries:
                    self.logger.debug(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                    last_exception = e
                    await asyncio.sleep(2 ** attempt)
                    continue

                # Last attempt, convert to custom exception
                self.logger.error("Request failed after %d attempts", self.max_retries + 1)

                # Check if it's a 5xx error from reverse proxy
                if e.response.status_code >= 500:
                    # Try to parse JSON response
                    try:
                        error_data = e.response.json()
                        if isinstance(error_data, dict) and "message" in error_data:
                            # Structured API error response
                            raise LybicAPIError(
                                message=error_data.get("message", "Unknown error"),
                                code=error_data.get("code"),
                                status_code=e.response.status_code,
                            ) from e
                    except (json.JSONDecodeError, ValueError):
                        # Not a JSON response, likely HTML from reverse proxy
                        pass

                    # If we got here, it's a reverse proxy error
                    raise LybicInternalError(status_code=e.response.status_code) from e

                # For 4xx errors, try to parse structured error response
                try:
                    error_data = e.response.json()
                    if isinstance(error_data, dict) and "message" in error_data:
                        raise LybicAPIError(
                            message=error_data.get("message", "Unknown error"),
                            code=error_data.get("code"),
                            status_code=e.response.status_code,
                        ) from e
                except (json.JSONDecodeError, ValueError):
                    # Not a JSON response, re-raise original exception
                    pass

                # If we couldn't parse it as a structured error, re-raise original
                raise
            except httpx.RequestError as e:
                last_exception = e
                if attempt < self.max_retries:
                    self.logger.debug(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                else:
                    self.logger.error("Request failed after %d attempts", self.max_retries + 1)
                await asyncio.sleep(2 ** attempt)

        raise last_exception
