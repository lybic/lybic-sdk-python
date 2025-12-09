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
lybic_sync.tools:
Synchronous ComputerUse tools
Synchronous MobileUse tools
"""
from typing import TYPE_CHECKING

from lybic.dto import (
    ParseTextRequestDto,
    ComputerUseActionResponseDto,
    ModelType,
    MobileUseActionResponseDto,
)

if TYPE_CHECKING:
    from lybic_sync.lybic_sync import LybicSyncClient

class ComputerUseSync:
    """ComputerUseSync is a synchronous client for lybic ComputerUse API(MCP and Restful)."""
    def __init__(self, client: "LybicSyncClient"):
        self.client = client

    def parse_llm_output(
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

        response = self.client.request(
            "POST",
            f"/api/computer-use/parse/{model}",
            json=ParseTextRequestDto(textContent=llm_output).model_dump(exclude_none=True),
        )
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return ComputerUseActionResponseDto.model_validate_json(response.text)

class MobileUseSync:
    """MobileUseSync is a synchronous client for lybic MobileUse API(MCP and Restful)."""
    def __init__(self, client: "LybicSyncClient"):
        self.client = client

    def parse_llm_output(
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

        response = self.client.request(
            "POST",
            f"/api/mobile-use/parse/{model}",
            json=ParseTextRequestDto(textContent=llm_output).model_dump(exclude_none=True),
        )
        self.client.logger.debug(f"Parse model output response: {response.text}")
        return MobileUseActionResponseDto.model_validate_json(response.text)

class ToolsSync:
    """ToolsSync is a container for various synchronous tool clients."""
    def __init__(self, client: "LybicSyncClient"):
        self.computer_use = ComputerUseSync(client)
        self.mobile_use = MobileUseSync(client)
