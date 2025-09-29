# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
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
"""Agentic Lybic Restful API client"""
import asyncio
import logging

import httpx

from lybic import LybicAuth
from lybic.gui_agents.models import (
    AgentInfo,
    CommonConfig,
    SetCommonConfigResponse,
    LLMConfig,
    RunAgentInstructionRequest,
    TaskStream,
    RunAgentInstructionAsyncResponse,
    QueryTaskStatusResponse
)


class Client:
    """Agentic Lybic Restful API client"""
    def __init__(self, auth: LybicAuth,timeout: int = 10,max_retries: int = 3):
        """Agentic Lybic Restful API client"""
        self.auth = auth
        self.timeout = timeout
        self.max_retries = max_retries
        self._httpclient: httpx.AsyncClient | None = None
        self._in_context = False
        self.logger = logging.getLogger(__name__)

    def _ensure_client_is_open(self):
        if self._httpclient is None:
            self._httpclient = httpx.AsyncClient(headers=self.auth.headers, timeout=self.timeout)
        elif self._httpclient.is_closed:
            raise RuntimeError("The client has been closed and cannot be reused. Please create a new client instance.")

    async def __aenter__(self):
        if self._in_context:
            raise RuntimeError("Cannot re-enter context.")
        if self._httpclient and not self._httpclient.is_closed:
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
        if self._httpclient:
            await self._httpclient.aclose()

    async def _get(self, path: str) -> httpx.Response:
        """
        Make a request to Lybic Restful API

        :param path: API endpoint
        :return: httpx.Response object
        """
        self._ensure_client_is_open()

        url = f"{self.auth.agent_service_endpoint}{path}"
        headers = self.auth.headers.copy()
        headers.pop("Content-Type", None)
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._httpclient.get(url, headers=headers)
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    self.logger.debug(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                else:
                    self.logger.error("Request failed after %d attempts", self.max_retries + 1)
                await asyncio.sleep(2 ** attempt)

        raise last_exception

    async def _post(self, path: str, data: dict) -> httpx.Response:
        """
        Make a request to Lybic Restful API

        :param path: API endpoint
        :param data: request data
        :return: httpx.Response object
        """
        self._ensure_client_is_open()

        url = f"{self.auth.agent_service_endpoint}{path}"
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                response = await self._httpclient.post(url, headers=self.auth.headers,json= data)
                response.raise_for_status()
                return response
            except (httpx.RequestError, httpx.HTTPStatusError) as e:
                last_exception = e
                if attempt < self.max_retries:
                    self.logger.debug(f"Request failed (attempt {attempt + 1}/{self.max_retries + 1}): {e}")
                else:
                    self.logger.error("Request failed after %d attempts", self.max_retries + 1)
                await asyncio.sleep(2 ** attempt)

        raise last_exception

    async def _stream(self, path: str, data: dict | None = None):
        """
        Make a streaming request to the Lybic Restful API (SSE).

        :param path: API endpoint.
        :param data: Optional request data. If provided, a POST request is made. Otherwise, a GET request is made.
        """
        self._ensure_client_is_open()

        url = f"{self.auth.agent_service_endpoint}{path}"
        headers = self.auth.headers.copy()

        method = "POST" if data else "GET"
        request_kwargs = {"headers": headers}
        if data:
            request_kwargs["json"] = data
        else:
            # No content-type for GET requests with no body
            headers.pop("Content-Type", None)

        async with self._httpclient.stream(method, url, **request_kwargs) as response:
            response.raise_for_status()
            async for line in response.aiter_lines():
                if line.strip() and line.startswith("data:"):
                    yield line[len("data:"):].strip()

    async def get_agent_info(self) -> AgentInfo:
        """
        Get agent info
        :return:
        """
        response = await self._get("/api/agent/info")
        return AgentInfo.model_validate_json(response.text)

    async def get_global_common_config(self) -> CommonConfig:
        """
        Get global common config
        :return:
        """
        response = await self._get("/api/agent/config/global")
        return CommonConfig.model_validate_json(response.text)

    async def set_global_common_config(self, config: CommonConfig) -> SetCommonConfigResponse:
        """
        Set global common config
        :param config:
        :return:
        """
        response = await self._post("/api/agent/config/global", data=config.model_dump())
        return SetCommonConfigResponse.model_validate_json(response.text)

    async def get_common_config(self, config_id: str) -> CommonConfig:
        """
        Get common config by id
        :param config_id:
        :return:
        """
        response = await self._get(f"/api/agent/config/{config_id}")
        return CommonConfig.model_validate_json(response.text)

    async def set_global_common_llm_config(self, config: LLMConfig) -> LLMConfig:
        """
        Set global common llm config
        :param config:
        :return:
        """
        response = await self._post("/api/agent/config/global/llm", data=config.model_dump())
        return LLMConfig.model_validate_json(response.text)

    async def get_global_grounding_llm_config(self) -> LLMConfig:
        """
        Get global grounding llm config
        :return:
        """
        response = await self._get("/api/agent/config/global/grounding-llm")
        return LLMConfig.model_validate_json(response.text)

    async def set_global_grounding_llm_config(self, config: LLMConfig) -> LLMConfig:
        """
        Set global grounding llm config
        :param config:
        :return:
        """
        response = await self._post("/api/agent/config/global/grounding-llm", data=config.model_dump())
        return LLMConfig.model_validate_json(response.text)

    async def set_global_embedding_llm_config(self, config: LLMConfig) -> LLMConfig:
        """
        Set global embedding llm config
        :param config:
        :return:
        """
        response = await self._post("/api/agent/config/global/embedding-llm", data=config.model_dump())
        return LLMConfig.model_validate_json(response.text)

    async def run_agent_instruction(self, request: RunAgentInstructionRequest):
        """
        Run agent instruction
        :param request:
        :return:
        """
        async for line in self._stream("/api/agent/run", data=request.model_dump()):
            yield TaskStream.model_validate_json(line)

    async def run_agent_instruction_async(self, request: RunAgentInstructionRequest) -> RunAgentInstructionAsyncResponse:
        """
        Run agent instruction async
        :param request:
        :return:
        """
        response = await self._post("/api/agent/run-async", data=request.model_dump())
        return RunAgentInstructionAsyncResponse.model_validate_json(response.text)

    async def get_agent_task_stream(self, task_id: str):
        """
        Get agent task stream
        :param task_id:
        :return:
        """
        async for line in self._stream(f"/api/agent/tasks/{task_id}/stream"):
            yield TaskStream.model_validate_json(line)

    async def query_task_status(self, task_id: str) -> QueryTaskStatusResponse:
        """
        Query task status
        :param task_id:
        :return:
        """
        response = await self._get(f"/api/agent/tasks/{task_id}/status")
        return QueryTaskStatusResponse.model_validate_json(response.text)
