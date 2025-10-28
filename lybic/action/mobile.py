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

"""Mobile action types."""
import uuid
from typing import Literal, Optional
from pydantic import BaseModel, Field

from .common import Length, json_extra_fields_policy

# pylint: disable=invalid-name


class MobileTapAction(BaseModel):
    """
    Represents a mobile tap action.
    """
    type: Literal["mobile:tap"]
    x: Length
    y: Length
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileDoubleTapAction(BaseModel):
    """
    Represents a mobile double tap action.
    """
    type: Literal["mobile:doubleTap"]
    x: Length
    y: Length
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileSwipeAction(BaseModel):
    """
    Represents a mobile swipe action.
    """
    type: Literal["mobile:swipe"]
    startX: Length
    startY: Length
    endX: Length
    endY: Length
    duration: int
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileTypeAction(BaseModel):
    """
    Represents a mobile type action.
    """
    type: Literal["mobile:type"]
    content: str
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileHotkeyAction(BaseModel):
    """
    Represents a mobile hotkey action.
    """
    type: Literal["mobile:hotkey"]
    key: str
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileHomeAction(BaseModel):
    """
    Represents a mobile home action.
    """
    type: Literal["mobile:home"]
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileBackAction(BaseModel):
    """
    Represents a mobile back action.
    """
    type: Literal["mobile:back"]
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileScreenshotAction(BaseModel):
    """
    Represents a mobile screenshot action.
    """
    type: Literal["mobile:screenshot"]
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileWaitAction(BaseModel):
    """
    Represents a mobile wait action.
    """
    type: Literal["mobile:wait"]
    duration: int
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileFinishedAction(BaseModel):
    """
    Represents a mobile finished action.
    """
    type: Literal["mobile:finished"]
    message: Optional[str] = None
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True

class MobileFailedAction(BaseModel):
    """
    Represents a mobile failed action.
    """
    type: Literal["mobile:failed"]
    message: Optional[str] = None
    callId: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()))
    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True
