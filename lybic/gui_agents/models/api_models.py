from pydantic import BaseModel
from typing import Optional
from enum import Enum, unique


@unique
class SandboxOS(str, Enum):
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    ANDROID = "ANDROID"

@unique
class InstanceMode(str, Enum):
    NORMAL = "NORMAL"
    FAST = "FAST"

@unique
class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILURE = "FAILURE"
    NOT_FOUND = "NOT_FOUND"

class AgentInfo(BaseModel):
    version: str
    maxConcurrentTasks: Optional[int] = None
    logLevel: Optional[str] = None
    domain: Optional[str] = None

class Sandbox(BaseModel):
    id: str
    name: str
    description: str
    shapeName: str
    hardwareAcceleratedEncoding: bool
    os: SandboxOS
    virtualization: str
    architecture: str

class Authorization(BaseModel):
    apiEndpoint: str
    orgID: Optional[str] = None
    apiKey: Optional[str] = None

class LLMConfig(BaseModel):
    modelName: str
    provider: str
    apiEndpoint: str
    apiKey: Optional[str] = None

class StageModelConfig(BaseModel):
    webSearchEngine: Optional[str] = None
    contextFusionModel: Optional[LLMConfig] = None
    subtaskPlannerModel: Optional[LLMConfig] = None
    trajReflectorModel: Optional[LLMConfig] = None
    memoryRetrivalModel: Optional[LLMConfig] = None
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

class CommonConfig(BaseModel):
    id: str
    backend: str
    mode: Optional[InstanceMode] = None
    steps: Optional[int] = None
    taskTimeout: Optional[int] = None
    authorizationInfo: Optional[Authorization] = None
    stageModelConfig: Optional[StageModelConfig] = None

class RunAgentInstructionRequest(BaseModel):
    instruction: str
    sandbox: Optional[Sandbox] = None
    runningConfig: Optional[CommonConfig] = None

class RunAgentInstructionAsyncResponse(BaseModel):
    taskId: str

class QueryTaskStatusResponse(BaseModel):
    taskId: str
    status: TaskStatus
    message: Optional[str] = None
    result: Optional[str] = None
    sandbox: Optional[Sandbox] = None

class TaskStream(BaseModel):
    taskId: str
    stage: str
    message: str

class SetCommonConfigResponse(BaseModel):
    success: bool
    id: str
