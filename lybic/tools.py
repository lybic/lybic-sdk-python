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
"""
lybic.tools:
ComputerUse tools
MobileUse tools
"""
from typing import overload

from lybic.dto import (
    ParseTextRequestDto,
    ComputerUseParseRequestDto,
    ComputerUseActionResponseDto,
    ModelType,
    ComputerUseActionDto,
    SandboxActionResponseDto,
    MobileUseActionResponseDto
)
from lybic.lybic import LybicClient
from lybic._api import deprecated

class ComputerUse:
    """ComputerUse is an async client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Use parse_llm_output instead"
    )
    @overload
    async def parse_model_output(self, data: ComputerUseParseRequestDto) -> ComputerUseActionResponseDto: ...
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Use parse_llm_output instead"
    )
    @overload
    async def parse_model_output(self, **kwargs) -> ComputerUseActionResponseDto: ...
    @deprecated(
        since="0.7.0",
        removal="1.0.0",
        message="Use parse_llm_output instead"
    )
    async def parse_model_output(self, *args, **kwargs) -> ComputerUseActionResponseDto:
        """
        parse doubao-ui-tars output

        :param data:
        :return:
        """
        if args and isinstance(args[0], ComputerUseParseRequestDto):
            data = args[0]
        elif "data" in kwargs and isinstance(kwargs["data"], ComputerUseParseRequestDto):
            data = kwargs["data"]
        else:
            data = ComputerUseParseRequestDto(**kwargs)
        self.client.logger.debug(f"Parse model output request: {data.model_dump_json()}")
        response = await self.client.request(
            "POST",
            "/api/computer-use/parse",
            json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return ComputerUseActionResponseDto.model_validate_json(response.text)
    async def parse_llm_output(
        self, model_type: ModelType | str, llm_output: str
    ) -> ComputerUseActionResponseDto:
        """Parse LLM output to computer use actions.

        Args:
            model_type: The type of the large language model.
            llm_output: The text output from the large language model.

        Returns:
            A DTO containing the parsed computer use actions.
        """
        if isinstance(model_type, ModelType):
            model = model_type.value
        elif isinstance(model_type, str):
            valid_models = [item.value for item in ModelType]
            if model_type not in valid_models:
                raise ValueError(f"Invalid model_type: {model_type}. Must be one of {valid_models}")
            model = model_type
        else:
            raise TypeError("model_type must be either dto.ModelType or str")

        response = await self.client.request(
            "POST",
            f"/api/computer-use/parse/{model}",
            json=ParseTextRequestDto(textContent=llm_output).model_dump(),
        )
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return ComputerUseActionResponseDto.model_validate_json(response.text)

    @deprecated(
        since="0.8.0",
        removal="1.0.0",
        message="Use `lybic.sandbox.Sandbox.execute_sandbox_action` instead."
    )
    @overload
    async def execute_computer_use_action(self, sandbox_id: str,
                                    data: ComputerUseActionDto) -> SandboxActionResponseDto: ...
    @deprecated(
        since="0.8.0",
        removal="1.0.0",
        message="Use `lybic.sandbox.Sandbox.execute_sandbox_action` instead."
    )
    @overload
    async def execute_computer_use_action(self, sandbox_id: str, **kwargs) -> SandboxActionResponseDto: ...

    @deprecated(
        since="0.8.0",
        removal="1.0.0",
        message="Use `lybic.sandbox.Sandbox.execute_sandbox_action` instead."
    )
    async def execute_computer_use_action(self, sandbox_id: str, *args, **kwargs) -> SandboxActionResponseDto:
        """Executes a computer use action in a specific sandbox.

        Note: This method provides the same functionality as
        `lybic.sandbox.Sandbox.execute_computer_use_action`.

        Args:
            sandbox_id: The ID of the sandbox to execute the action in.
            *args: Supports passing `dto.ComputerUseActionDto` as a positional argument.
            **kwargs: Supports passing `data` as a `dto.ComputerUseActionDto` or a `dict`,
                or the fields of `dto.ComputerUseActionDto` directly as keyword arguments.

        Returns:
            A `dto.SandboxActionResponseDto` containing the result of the action.

        Raises:
            TypeError: If the 'data' argument is not of the expected type.
        """
        if args and isinstance(args[0], ComputerUseActionDto):
            data = args[0]
        elif "data" in kwargs:
            data_arg = kwargs["data"]
            if isinstance(data_arg, ComputerUseActionDto):
                data = data_arg
            elif isinstance(data_arg, dict):
                data = ComputerUseActionDto(**data_arg)
            else:
                raise TypeError(f"The 'data' argument must be of type {ComputerUseActionDto.__name__} or dict")
        else:
            data = ComputerUseActionDto(**kwargs)
        self.client.logger.debug(f"Execute computer use action request: {data.model_dump_json()}")
        response = await self.client.request("POST",
                                       f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/actions/computer-use",
                                       json=data.model_dump(exclude_none=True))
        self.client.logger.debug(f"Execute computer use action response: {response.text}")
        return SandboxActionResponseDto.model_validate_json(response.text)

class MobileUse:
    """MobileUse is an async client for lybic MobileUse API(MCP and Restful)."""
    def __init__(self, client: LybicClient):
        self.client = client

    async def parse_llm_output(
        self, model_type: ModelType | str, llm_output: str
    ) -> MobileUseActionResponseDto:
        """Parse LLM output to mobile use actions.

        Args:
            model_type: The type of the large language model.
            llm_output: The text output from the large language model.

        Returns:
            A DTO containing the parsed mobile use actions.
        """
        if isinstance(model_type, ModelType):
            model = model_type.value
        elif isinstance(model_type, str):
            valid_models = [item.value for item in ModelType]
            if model_type not in valid_models:
                raise ValueError(f"Invalid model_type: {model_type}. Must be one of {valid_models}")
            model = model_type
        else:
            raise TypeError("model_type must be either dto.ModelType or str")

        response = await self.client.request(
            "POST",
            f"/api/mobile-use/parse/{model}",
            json=ParseTextRequestDto(textContent=llm_output).model_dump(),
        )
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return MobileUseActionResponseDto.model_validate_json(response.text)
