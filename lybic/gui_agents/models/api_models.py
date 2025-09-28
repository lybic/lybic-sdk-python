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
"""Agentic Lybic Restful API models"""
from typing import Optional
from enum import Enum, unique

from pydantic import BaseModel

@unique
class SandboxOS(str, Enum):
    """Sandbox os type"""
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    ANDROID = "ANDROID"

@unique
class InstanceMode(str, Enum):
    """Agentic Lybic task instance executing mode"""
    NORMAL = "NORMAL"
    FAST = "FAST"

@unique
class TaskStatus(str, Enum):
    """Agentic Lybic task status"""
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    NOT_FOUND = "NOT_FOUND"

class AgentInfo(BaseModel):
    """Agentic Lybic agent info"""
    version: str
    maxConcurrentTasks: Optional[int] = None
    logLevel: Optional[str] = None
    domain: Optional[str] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class Sandbox(BaseModel):
    """sandbox info for task executing platform"""
    id: str
    name: str
    description: str
    shapeName: str
    hardwareAcceleratedEncoding: bool
    os: SandboxOS
    virtualization: str
    architecture: str
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class Authorization(BaseModel):
    """Lybic API authorization info"""
    apiEndpoint: str
    orgID: Optional[str] = None
    apiKey: Optional[str] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class LLMConfig(BaseModel):
    """LLM model config"""
    modelName: str
    provider: str
    apiEndpoint: str
    apiKey: Optional[str] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class StageModelConfig(BaseModel):
    """Stage model config"""
    webSearchEngine: Optional[str] = None
    contextFusionModel: Optional[LLMConfig] = None
    subtaskPlannerModel: Optional[LLMConfig] = None
    trajReflectorModel: Optional[LLMConfig] = None
    memoryRetrievalModel: Optional[LLMConfig] = None
    groundingModel: Optional[LLMConfig] = None
    taskEvaluatorModel: Optional[LLMConfig] = None
    actionGeneratorModel: Optional[LLMConfig] = None
    actionGeneratorWithTakeoverModel: Optional[LLMConfig] = None
    fastActionGeneratorModel: Optional[LLMConfig] = None
    fastActionGeneratorWithTakeoverModel: Optional[LLMConfig] = None
    dagTranslatorModel: Optional[LLMConfig] = None
    embeddingModel: Optional[LLMConfig] = None
    queryFormulatorModel: Optional[LLMConfig] = None
    narrativeSummarizationModel: Optional[LLMConfig] = None
    textSpanModel: Optional[LLMConfig] = None
    episodeSummarizationModel: Optional[LLMConfig] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class CommonConfig(BaseModel):
    """Agentic Lybic common config"""
    id: str
    backend: str
    mode: Optional[InstanceMode] = None
    steps: Optional[int] = None
    taskTimeout: Optional[int] = None
    authorizationInfo: Optional[Authorization] = None
    stageModelConfig: Optional[StageModelConfig] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class RunAgentInstructionRequest(BaseModel):
    """Agentic Lybic run agent instruction request"""
    instruction: str
    sandbox: Optional[Sandbox] = None
    runningConfig: Optional[CommonConfig] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        exclude_none = True

class RunAgentInstructionAsyncResponse(BaseModel):
    """Agentic Lybic run agent instruction async response"""
    taskId: str
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"

class QueryTaskStatusResponse(BaseModel):
    """Agentic Lybic query task status response"""
    taskId: str
    status: TaskStatus
    message: Optional[str] = None
    result: Optional[str] = None
    sandbox: Optional[Sandbox] = None
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
        exclude_none = True

class TaskStream(BaseModel):
    """Agentic Lybic task stream"""
    taskId: str
    stage: str
    message: str
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"

class SetCommonConfigResponse(BaseModel):
    """Agentic Lybic set common config response"""
    success: bool
    id: str
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = "ignore"
