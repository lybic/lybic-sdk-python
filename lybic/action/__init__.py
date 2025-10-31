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

"""Action types for Lybic SDK."""

from typing import Union

# Common types
from .common import (
    PixelLength,
    FractionalLength,
    Length,
    ClientUserTakeoverAction,
    ScreenshotAction,
    WaitAction,
    FinishedAction,
    FailedAction,
    CommonAction,
)

# Computer use actions
from .computer import (
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
    ComputerUseAction,
)

# Touch actions
from .touch import (
    TouchTapAction,
    TouchDragAction,
    TouchSwipeAction,
    TouchLongPressAction,
)

# Android actions
from .android import (
    AndroidBackAction,
    AndroidHomeAction,
)

# OS actions
from .os import (
    OsStartAppAction,
    OsStartAppByNameAction,
    OsCloseAppAction, OsListAppsAction,
)

# Mobile-specific actions remain with "mobile:" prefix for backward compatibility
MobileUseAction = Union[
    ScreenshotAction,        # generalActionScreenshotSchema
    WaitAction,              # generalActionWaitSchema
    FinishedAction,          # generalActionFinishedSchema
    FailedAction,            # generalActionFailedSchema
    ClientUserTakeoverAction, # generalActionUserTakeoverSchema

    KeyboardTypeAction, # generalActionKeyboardTypeSchema
    KeyboardHotkeyAction, # generalActionKeyboardHotkeySchema

    TouchTapAction, # mobileUseActionTapSchema
    TouchDragAction,  # mobileUseActionDragSchema
    TouchSwipeAction, # mobileUseActionSwipeSchema
    TouchLongPressAction, # mobileUseActionLongPressSchema
    AndroidBackAction, # mobileUseActionPressBackSchema
    AndroidHomeAction, # mobileUseActionPressHomeSchema

    OsStartAppAction, # mobileUseActionStartAppSchema
    OsStartAppByNameAction, # mobileUseActionStartAppByNameSchema
    OsCloseAppAction, # mobileUseActionCloseAppSchema
    OsListAppsAction, # mobileUseActionListAppsSchema
]


Action = Union[ComputerUseAction, MobileUseAction]


__all__ = [
    # Common types
    "PixelLength",
    "FractionalLength",
    "Length",
    "ClientUserTakeoverAction",
    "ScreenshotAction",
    "WaitAction",
    "FinishedAction",
    "FailedAction",
    "CommonAction",

    # Computer use actions
    "MouseClickAction",
    "MouseTripleClickAction",
    "MouseDoubleClickAction",
    "MouseMoveAction",
    "MouseScrollAction",
    "MouseDragAction",
    "KeyboardTypeAction",
    "KeyboardHotkeyAction",
    "KeyDownAction",
    "KeyUpAction",
    "ComputerUseAction",

    # Touch actions
    "TouchTapAction",
    "TouchDragAction",
    "TouchSwipeAction",
    "TouchLongPressAction",

    # Android actions
    "AndroidBackAction",
    "AndroidHomeAction",

    # OS actions
    "OsStartAppAction",
    "OsStartAppByNameAction",
    "OsCloseAppAction",
    "OsListAppsAction",

    # Union types
    "MobileUseAction",
    "Action",
]
