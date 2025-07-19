from pydantic import BaseModel, Field
from typing import List, Optional, Union, Literal

# General Schemas
class StatsResponseDto(BaseModel):
    pass

# MCP Schemas
class McpServerPolicy(BaseModel):
    sandboxMaxLifetimeSeconds: int = Field(3600, description="The maximum lifetime of a sandbox.")
    sandboxMaxIdleTimeSeconds: int = Field(3600, description="The maximum idle time of a sandbox.")
    sandboxAutoCreation: bool = Field(False, description="Whether to create a new sandbox automatically when old sandbox is deleted. If not, new sandboxes will be created when calling computer use tools.")
    sandboxExposeRecreateTool: bool = Field(False, description="Whether to expose recreate tool to LLMs.")
    sandboxExposeRestartTool: bool = Field(False, description="Whether to expose restart tool to LLMs.")
    sandboxExposeDeleteTool: bool = Field(False, description="Whether to expose delete tool to LLMs.")

class McpServerResponseDto(BaseModel):
    id: str = Field(..., description="ID of the MCP server.")
    name: str = Field(..., description="Name of the MCP server.")
    createdAt: str = Field(..., description="Creation date of the MCP server.")
    defaultMcpServer: bool = Field(..., description="Whether this is the default MCP server for the organization.")
    projectId: str = Field(..., description="Project ID to which the MCP server belongs.")
    policy: McpServerPolicy

class ListMcpServerResponse(BaseModel):
    __root__: List[McpServerResponseDto]

class CreateMcpServerDto(McpServerPolicy, BaseModel):
    name: str = Field(..., description="Name of the MCP server.")
    projectId: Optional[str] = Field(None, description="Project to which the MCP server belongs to.")
    sandboxMaxLifetimeSeconds: int = Field(3600, description="The maximum lifetime of a sandbox.")
    sandboxMaxIdleTimeSeconds: int = Field(3600, description="The maximum idle time of a sandbox.")
    sandboxAutoCreation: bool = Field(False, description="Whether to create a new sandbox automatically when old sandbox is deleted. If not, new sandboxes will be created when calling computer use tools.")
    sandboxExposeRecreateTool: bool = Field(False, description="Whether to expose recreate tool to LLMs.")
    sandboxExposeRestartTool: bool = Field(False, description="Whether to expose restart tool to LLMs.")
    sandboxExposeDeleteTool: bool = Field(False, description="Whether to expose delete tool to LLMs.")

# Sandbox Schemas
class Sandbox(BaseModel):
    id: str = Field(..., description="ID of the sandbox.")
    name: str = Field(..., description="Name of the sandbox.")
    expiredAt: str = Field(..., description="Expiration date of the sandbox.")
    createdAt: str = Field(..., description="Creation date of the sandbox.")
    projectId: str = Field(..., description="Project ID to which the sandbox belongs.")

class GatewayAddress(BaseModel):
    address: str
    port: int
    name: str
    preferredProviders: List[Literal["CHINA_MOBILE", "CHINA_UNICOM", "CHINA_TELECOM", "GLOBAL_BGP", 1, 2, 3, 4]]
    gatewayType: Literal["KCP", "QUIC", "WEB_TRANSPORT", 4, 5, 6]

class ConnectDetails(BaseModel):
    gatewayAddresses: List[GatewayAddress]
    certificateHashBase64: str
    endUserToken: str

class SandboxListItem(BaseModel):
    sandbox: Sandbox
    connectDetails: ConnectDetails

class SandboxListResponseDto(BaseModel):
    __root__: List[SandboxListItem]

class CreateSandboxDto(BaseModel):
    name: str = Field("sandbox", description="The name of the sandbox.")
    maxLifeSeconds: int = Field(3600, description="The maximum life time of the sandbox in seconds. Default is 1 hour, max is 1 day.", ge=1, le=86400)
    projectId: Optional[str] = Field(None, description="The project id to use for the sandbox. Use default if not provided.")
    specId: Optional[str] = Field(None, description="The spec of the sandbox. Use default if not provided.")
    datacenterId: Optional[str] = Field(None, description="The datacenter id to use for the sandbox. Use default if not provided.")

class GetSandboxResponseDto(BaseModel):
    sandbox: Sandbox
    connectDetails: ConnectDetails

# Computer Use Schemas
class PixelLength(BaseModel):
    type: Literal["px"]
    value: int

class FractionalLength(BaseModel):
    type: Literal["/"]
    numerator: int
    denominator: int

Length = Union[PixelLength, FractionalLength]

class MouseClickAction(BaseModel):
    type: Literal["mouse:click"]
    x: Length
    y: Length
    button: int

class MouseDoubleClickAction(BaseModel):
    type: Literal["mouse:doubleClick"]
    x: Length
    y: Length
    button: int

class MouseMoveAction(BaseModel):
    type: Literal["mouse:move"]
    x: Length
    y: Length

class MouseScrollAction(BaseModel):
    type: Literal["mouse:scroll"]
    x: Length
    y: Length
    stepVertical: int
    stepHorizontal: int

class MouseDragAction(BaseModel):
    type: Literal["mouse:drag"]
    startX: Length
    startY: Length
    endX: Length
    endY: Length

class KeyboardTypeAction(BaseModel):
    type: Literal["keyboard:type"]
    content: str

class KeyboardHotkeyAction(BaseModel):
    type: Literal["keyboard:hotkey"]
    keys: str

class ScreenshotAction(BaseModel):
    type: Literal["screenshot"]

class WaitAction(BaseModel):
    type: Literal["wait"]
    duration: int

class FinishedAction(BaseModel):
    type: Literal["finished"]
    message: Optional[str] = None

class FailedAction(BaseModel):
    type: Literal["failed"]
    message: Optional[str] = None

ComputerUseAction = Union[
    MouseClickAction,
    MouseDoubleClickAction,
    MouseMoveAction,
    MouseScrollAction,
    MouseDragAction,
    KeyboardTypeAction,
    KeyboardHotkeyAction,
    ScreenshotAction,
    WaitAction,
    FinishedAction,
    FailedAction,
]

class ComputerUseActionDto(BaseModel):
    action: ComputerUseAction
    includeScreenShot: bool = True
    includeCursorPosition: bool = True
    callId: Optional[str] = None

class CursorPosition(BaseModel):
    x: int
    y: int
    screenWidth: int
    screenHeight: int
    screenIndex: int

class SandboxActionResponseDto(BaseModel):
    screenShot: str
    cursorPosition: CursorPosition

class ComputerUseParseRequestDto(BaseModel):
    model: Literal["ui-tars", "oai-compute-use"]
    textContent: str
    output: Optional[List] = None

class ComputerUseActionResponseDto(BaseModel):
    actions: List[ComputerUseAction]

# Project Schemas
class ProjectResponseDto(BaseModel):
    id: str
    name: str
    createdAt: str
    defaultProject: bool

class ListProjectsResponseDto(BaseModel):
    __root__: List[ProjectResponseDto]

class CreateProjectDto(BaseModel):
    name: str

class SingleProjectResponseDto(ProjectResponseDto):
    pass