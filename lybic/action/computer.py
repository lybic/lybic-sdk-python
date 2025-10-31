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

"""Computer use action types."""
from typing import Literal, Optional, Union
from pydantic import BaseModel, Field

from .common import Length, json_extra_fields_policy, ScreenshotAction, WaitAction, FinishedAction, FailedAction, ClientUserTakeoverAction

class MouseClickAction(BaseModel):
    """
    Represents a mouse click action at a specified location.
    """
    type: Literal["mouse:click"] = "mouse:click"
    x: Length
    y: Length
    button: int = Field(..., description="Mouse button flag combination. 1: left, 2: right, 4: middle, 8: back, 16: forward; add them together to press multiple buttons at once.")
    relative: bool = Field(False, description="Whether the coordinates are relative to the current mouse position")
    holdKey: Optional[str] = Field(None, description="Key to hold down during click, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MouseTripleClickAction(BaseModel):
    """
    Represents a mouse triple-click action at a specified location.
    """
    type: Literal["mouse:tripleClick"] = "mouse:tripleClick"
    x: Length
    y: Length
    button: int = Field(..., description="Mouse button flag combination. 1: left, 2: right, 4: middle, 8: back, 16: forward; add them together to press multiple buttons at once.")
    relative: bool = Field(False, description="Whether the coordinates are relative to the current mouse position.")
    holdKey: Optional[str] = Field(None, description="Key to hold down during triple click, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MouseDoubleClickAction(BaseModel):
    """
    Represents a mouse double-click action at a specified location.
    """
    type: Literal["mouse:doubleClick"] = "mouse:doubleClick"
    x: Length
    y: Length
    button: int = Field(..., description="Mouse button flag combination. 1: left, 2: right, 4: middle, 8: back, 16: forward; add them together to press multiple buttons at once.")
    relative: bool = Field(False, description="Whether the coordinates are relative to the current mouse position")
    holdKey: Optional[str] = Field(None, description="Key to hold down during click, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class MouseMoveAction(BaseModel):
    """
    Represents a mouse move action to a specified location.
    """
    type: Literal["mouse:move"] = "mouse:move"
    x: Length
    y: Length
    relative: bool = Field(False, description="Whether the coordinates are relative to the current mouse position")
    holdKey: Optional[str] = Field(None, description="Key to hold down during move, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class MouseScrollAction(BaseModel):
    """
    Represents a mouse scroll action.
    """
    type: Literal["mouse:scroll"] = "mouse:scroll"
    x: Length
    y: Length
    stepVertical: int
    stepHorizontal: int
    relative: bool = Field(False, description="Whether the coordinates are relative to the current mouse position")
    holdKey: Optional[str] = Field(None, description="Key to hold down during scroll, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class MouseDragAction(BaseModel):
    """
    Represents a mouse drag action from a start to an end point.
    """
    type: Literal["mouse:drag"] = "mouse:drag"
    startX: Length
    startY: Length
    endX: Length
    endY: Length
    startRelative: bool = Field(False, description="Whether the start coordinates are relative to the current mouse position.")
    endRelative: bool = Field(False, description="Whether the end coordinates are relative to the start coordinates of the drag. If false, they are absolute screen coordinates.")
    button: int = Field(..., description="Mouse button flag combination. 1: left, 2: right, 4: middle, 8: back, 16: forward; add them together to press multiple buttons at once.")
    holdKey: Optional[str] = Field(None, description="Key to hold down during drag, in xdotool key syntax. Example: \"ctrl\", \"alt\", \"alt+shift\"")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class KeyboardTypeAction(BaseModel):
    """
    Represents a keyboard typing action.
    """
    type: Literal["keyboard:type"] =  "keyboard:type"
    content: str
    treatNewLineAsEnter: bool = Field(False, description="Whether to treat line breaks as enter. If true, any line breaks(\\n) in content will be treated as enter key press, and content will be split into multiple lines.")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class KeyboardHotkeyAction(BaseModel):
    """
    Represents a keyboard hotkey combination action.
    """
    type: Literal["keyboard:hotkey"] =  "keyboard:hotkey"
    keys: str
    duration: Optional[int] = Field(None, description="Duration in milliseconds. If specified, the hotkey will be held for a while and then released.")

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class KeyDownAction(BaseModel):
    """
    Press ONE key down, in xdotool key syntax. Only use this action if hotkey or type cannot satisfy your needs.
    """
    type: Literal["key:down"]= "key:down"
    key: str

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        validate_assignment = True
        exclude_none = True


class KeyUpAction(BaseModel):
    """
    Release ONE key, in xdotool key syntax. Only use this action if keydown cannot satisfy your needs and only after a key down.
    """
    type: Literal["key:up"] = "key:up"
    key: str

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        validate_assignment = True
        exclude_none = True


ComputerUseAction = Union[
    MouseClickAction,
    MouseTripleClickAction,
    MouseDoubleClickAction,
    MouseMoveAction,
    MouseScrollAction,
    MouseDragAction,

    KeyboardTypeAction,
    KeyboardHotkeyAction,
    KeyDownAction,
    KeyUpAction,

    ScreenshotAction,
    WaitAction,
    FinishedAction,
    FailedAction,
    ClientUserTakeoverAction,
]
