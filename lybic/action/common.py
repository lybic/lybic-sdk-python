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

"""Common action types and helper types."""
from typing import Literal, Optional, Union
from pydantic import BaseModel

# pylint: disable=invalid-name

# Strategy for handling extra fields in the lybic api response
json_extra_fields_policy = "ignore"


class PixelLength(BaseModel):
    """
    Represents a length in pixels.
    """
    type: Literal["px"] = "px"
    value: int

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        validate_assignment = True
        exclude_none = True


class FractionalLength(BaseModel):
    """
    Represents a length as a fraction of a total dimension.
    """
    type: Literal["/"] = "/"
    numerator: int
    denominator: int

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        validate_assignment = True
        exclude_none = True


Length = Union[PixelLength, FractionalLength]


class ClientUserTakeoverAction(BaseModel):
    """
    Indicates the human user should take over the control.
    """
    type: Literal["client:user-takeover"] = "client:user-takeover"

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class ScreenshotAction(BaseModel):
    """
    Represents an action to take a screenshot.
    """
    type: Literal["screenshot"] = "screenshot"

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class WaitAction(BaseModel):
    """
    Represents a wait action for a specified duration.
    """
    type: Literal["wait"] = "wait"
    duration: int

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class FinishedAction(BaseModel):
    """
    Represents a finished action, signaling successful completion of a task.
    """
    type: Literal["finished"] = "finished"
    message: Optional[str] = None

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


class FailedAction(BaseModel):
    """
    Represents a failed action, signaling an error or failure in a task.
    """
    type: Literal["failed"] = "failed"
    message: Optional[str] = None

    class Config:
        """
        Configuration for Pydantic model.
        """
        extra = json_extra_fields_policy
        # Allow population of fields with default values
        validate_assignment = True
        exclude_none = True


CommonAction = Union[
    ScreenshotAction,
    WaitAction,
    FinishedAction,
    FailedAction,
    ClientUserTakeoverAction,
]
