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
pyautogui.py implements a calling interface compatible with pyautogui.py through lybic

from lybic import LybicClient, Pyautogui

client = LybicClient()
pyautogui = Pyautogui(client, 'your-sandbox-id')

pyautogui.position()
pyautogui.moveTo(1443,343)
pyautogui.click()
pyautogui.click(x=1443, y=343)
pyautogui.rightClick()
pyautogui.middleClick()
pyautogui.tripleClick()
pyautogui.typewrite(['a', 'b', 'c', 'left', 'backspace', 'enter', 'f1'], interval=secs_between_keys)
pyautogui.move(None, 10)
pyautogui.doubleClick()
pyautogui.moveTo(500, 500)
pyautogui.write('Hello world!')
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')
pyautogui.scroll(100)
pyautogui.dragTo(500, 500)
"""
import asyncio
import logging
import re
import threading
import time
from typing import overload, Optional, Coroutine, List, Union

from lybic.lybic import LybicAuth, LybicClient
from lybic.action import (
    FinishedAction,
    MouseMoveAction,
    PixelLength,
    MouseDoubleClickAction,
    MouseClickAction,
    MouseDragAction,
    MouseScrollAction,
    KeyboardTypeAction,
    KeyboardHotkeyAction,
    KeyDownAction,
    KeyUpAction,
)
from lybic.dto import ExecuteSandboxActionDto
from lybic.sandbox import Sandbox

# pylint: disable=unused-argument,invalid-name,logging-fstring-interpolation
class Pyautogui:
    """
    Pyautogui implements a calling interface compatible with pyautogui.py through lybic

    Examples:

    LLM_OUTPUT = 'pyautogui.click(x=1443, y=343)'

    from lybic import LybicClient, Pyautogui

    client = LybicClient()

    pyautogui = Pyautogui(client,sandbox_id)

    eval(LLM_OUTPUT)
    """
    def __init__(self, client: LybicClient, sandbox_id: str):
        self._original_client = client
        self.logger = logging.getLogger(__name__)
        if client.client and not client.client.is_closed:
            self.logger.warning(
                "The provided LybicClient is already active. "
                "Pyautogui will create its own client instance to avoid event loop conflicts. "
                "For better performance, initialize Pyautogui with an inactive LybicClient."
            )
            self.client = LybicClient(
                LybicAuth(
                    org_id=client.org_id,
                    api_key=client._api_key,
                    endpoint=client.endpoint,
                    extra_headers=client.headers,
                ),
                timeout=client.timeout,
                max_retries=client.max_retries,
            )
        else:
            self.client = client

        self.sandbox = Sandbox(self.client)
        self.sandbox_id = sandbox_id

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self.logger.info("PyautoguiLybic event loop running in background thread.")

    def _run_sync(self, coro: Coroutine):
        """Runs a coroutine in the background event loop and waits for the result."""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result()

    def close(self):
        """Stops the background event loop and thread."""
        if self._thread.is_alive():
            self.logger.info("Closing PyautoguiLybic background event loop.")
            self._loop.call_soon_threadsafe(self._loop.stop)
            self._thread.join()
            self.logger.info("PyautoguiLybic background thread closed.")

    def __del__(self):
        self.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @staticmethod
    def parse(content: str) -> str:
        """
        Parses the given text content to extract pyautogui commands.

        Args:
            content (str): The text content to parse.

        Returns:
            str: A string containing the extracted pyautogui commands, each on a new line.
        """
        pattern = r"pyautogui\[a-zA-Z_]\w*\(.*\)"
        matches = re.findall(pattern, content)
        return "\n".join(matches)

    @overload
    def clone(self, sandbox_id: str) -> "Pyautogui": ...

    @overload
    def clone(self) -> "Pyautogui": ...

    def clone(self, sandbox_id: str = None) -> "Pyautogui":
        """
        Clones the Pyautogui object with a new sandbox ID.

        Args:
            sandbox_id (str, optional): The sandbox ID to clone the object with. If not provided, the original sandbox ID will be used.

        Returns:
            Pyautogui: A new Pyautogui object with the specified sandbox ID.
        Note: The cloned object will have its own background thread. Frequent cloning may lead to high resource consumption.
        """
        if sandbox_id is not None:
            return Pyautogui(self._original_client, sandbox_id)
        return Pyautogui(self._original_client, self.sandbox_id)

    def position(self) -> tuple[int, int]:
        """
        Returns the current mouse position.

        Returns:
            tuple[int, int]: The current mouse position as a tuple of (x, y).
        """
        return self.get_mouse_position()

    def get_mouse_position(self) -> tuple[int, int]:
        """
        Returns the current mouse position.

        Returns:
            tuple[int, int]: The current mouse position as a tuple of (x, y).
        """
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            # An action is required to obtain the mouse cursor and screenshot information.
            #
            # The `FinishedAction` , however, does not involve any action operations, is idempotent,
            # and offers the highest performance.
            data=ExecuteSandboxActionDto(
                action=FinishedAction(type="finished"),
                includeScreenShot=False,
                includeCursorPosition=True
            ),
        )
        result = self._run_sync(coro)
        if result.cursorPosition:
            return result.cursorPosition.x, result.cursorPosition.y
        raise ConnectionError("Could not get mouse position")

    def moveTo(self, x, y, duration=0.0, tween=None, logScreenshot=False, _pause=True):
        """
        Moves the mouse to the specified position.

        Args:
            x (int): The x-coordinate of the destination position.
            y (int): The y-coordinate of the destination position.
            duration (Placeholder):
            tween (Placeholder):
            logScreenshot (Placeholder):
            _pause (Placeholder):
        """
        request = MouseMoveAction(
            type="mouse:move",
            x=PixelLength(type="px", value=x),
            y=PixelLength(type="px", value=y),
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def move(self, xOffset=None, yOffset=None, duration=0.0, tween=None, _pause=True):
        """
        Moves the mouse relative to its current position.

        Args:
            xOffset (int, optional): The x-coordinate offset. If None, the current x-coordinate will be used.
            yOffset (int, optional): The y-coordinate offset. If None, the current y-coordinate will be used.
            duration (Placeholder):
            tween (Placeholder):
            _pause (Placeholder):
        """
        if xOffset is None and yOffset is None:
            return

        current_x, current_y = self.position()
        xOffset = xOffset if xOffset is not None else 0
        yOffset = yOffset if yOffset is not None else 0

        new_x = current_x + xOffset
        new_y = current_y + yOffset
        self.moveTo(new_x, new_y, duration, tween, _pause=_pause)

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              clicks=1, interval=0.0, button='left', duration=0.0, tween=None,
              logScreenshot=None, _pause=True):
        """
        Performs a mouse click at the specified position.

        Args:
            x (int, optional): The x-coordinate of the click position. If None, the current mouse position will be used.
            y (int, optional): The y-coordinate of the click position. If None, the current mouse position will be used.
            clicks (int, optional): The number of clicks to perform. Defaults to 1.
            interval (Placeholder):
            button (str, optional): The button to click. Can be 'left', 'right', or 'middle'. Defaults to 'left'.
        """
        if x is None or y is None:
            x, y = self.position()

        self.logger.info(f"click(x={x}, y={y}, clicks={clicks}, button='{button}')")

        button_map = {'left': 1, 'right': 2, 'middle': 4}
        button_code = button_map.get(button.lower(), 1)

        if clicks == 2:
            action = MouseDoubleClickAction(
                type="mouse:doubleClick",
                x=PixelLength(type="px", value=x),
                y=PixelLength(type="px", value=y),
                button=button_code
            )
            coro = self.sandbox.execute_sandbox_action(
                sandbox_id=self.sandbox_id,
                data=ExecuteSandboxActionDto(action=action, includeScreenShot=False,
                                              includeCursorPosition=False)
            )
            self._run_sync(coro)
        else:
            for i in range(clicks):
                action = MouseClickAction(
                    type="mouse:click",
                    x=PixelLength(type="px", value=x),
                    y=PixelLength(type="px", value=y),
                    button=button_code
                )

                coro = self.sandbox.execute_sandbox_action(
                    sandbox_id=self.sandbox_id,
                    data=ExecuteSandboxActionDto(action=action, includeScreenShot=False,
                                                  includeCursorPosition=False)
                )
                self._run_sync(coro)

                if i < clicks - 1:
                    time.sleep(interval)

    def doubleClick(self, x: Optional[int] = None, y: Optional[int] = None,
                    interval=0.0, button='left', duration=0.0, tween=None, _pause=True):
        """
        Performs a double-click at the specified position.

        Args:
            x (int, optional): The x-coordinate of the click position. If None, the current mouse position will be used.
            y (int, optional): The y-coordinate of the click position. If None, the current mouse position will be used.
            interval (Placeholder):
            button (str, optional): The button to click. Can be 'left', 'right', or 'middle'. Defaults to 'left'.
        """
        self.click(x, y, clicks=2, interval=interval, button=button, duration=duration, tween=tween, _pause=_pause)

    def rightClick(self, x: Optional[int] = None, y: Optional[int] = None,
                   duration: float = 0.0, tween=None, _pause: bool = True):
        """
        Performs a right-click at the specified position.

        Args:
            x (int, optional): The x-coordinate of the click position. If None, the current mouse position will be used.
            y (int, optional): The y-coordinate of the click position. If None, the current mouse position will be used.
            duration (float, optional): The time in seconds to spend moving the mouse. Defaults to 0.0. This parameter is currently ignored.
            tween (optional): The tweening function. This parameter is currently ignored.
            _pause (bool, optional): Whether to pause after the action. Defaults to True.
        """
        self.click(x, y, button='right', duration=duration, tween=tween, _pause=_pause)

    def middleClick(self, x: Optional[int] = None, y: Optional[int] = None,
                    duration: float = 0.0, tween=None, _pause: bool = True):
        """
        Performs a middle-click at the specified position.

        Args:
            x (int, optional): The x-coordinate of the click position. If None, the current mouse position will be used.
            y (int, optional): The y-coordinate of the click position. If None, the current mouse position will be used.
            duration (float, optional): The time in seconds to spend moving the mouse. Defaults to 0.0. This parameter is currently ignored.
            tween (optional): The tweening function. This parameter is currently ignored.
            _pause (bool, optional): Whether to pause after the action. Defaults to True.
        """
        self.click(x, y, button='middle', duration=duration, tween=tween, _pause=_pause)

    def tripleClick(self, x: Optional[int] = None, y: Optional[int] = None,
                    interval: float = 0.0, button: str = 'left', duration: float = 0.0, tween=None, _pause: bool = True):
        """
        Performs a triple-click at the specified position.

        Args:
            x (int, optional): The x-coordinate of the click position. If None, the current mouse position will be used.
            y (int, optional): The y-coordinate of the click position. If None, the current mouse position will be used.
            interval (float, optional): The time in seconds between clicks. Defaults to 0.0.
            button (str, optional): The button to click. Can be 'left', 'right', or 'middle'. Defaults to 'left'.
            duration (float, optional): The time in seconds to spend moving the mouse. Defaults to 0.0. This parameter is currently ignored.
            tween (optional): The tweening function. This parameter is currently ignored.
            _pause (bool, optional): Whether to pause after the action. Defaults to True.
        """
        self.click(x, y, clicks=3, interval=interval, button=button, duration=duration, tween=tween, _pause=_pause)

    def dragTo(self, x: int, y: int, duration: float = 0.0, button: str = 'left', _pause: bool = True):
        """
        Drags the mouse to the specified position.

        Args:
            x (int): The x-coordinate of the destination position.
            y (int): The y-coordinate of the destination position.
            duration (float, optional): The time in seconds to spend moving the mouse. Defaults to 0.0. This parameter is currently ignored.
            button (str, optional): The button to drag with. Can be 'left', 'right', or 'middle'. Defaults to 'left'.
        """
        if button.lower() != 'left':
            self.logger.warning(f"Lybic API currently only supports dragging with the left mouse button, but '{button}' was requested. Proceeding with left button.")

        start_x, start_y = self.position()

        self.logger.info(f"dragTo(x={x}, y={y}, button='{button}')")

        request = MouseDragAction(
            type="mouse:drag",
            startX=PixelLength(type="px", value=start_x),
            startY=PixelLength(type="px", value=start_y),
            endX=PixelLength(type="px", value=x),
            endY=PixelLength(type="px", value=y)
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None, _pause: bool = True):
        """
        Scrolls the mouse wheel.
        Args:
            clicks (int): The amount of scrolling to perform. Positive values scroll up, negative values scroll down.
            x (int, optional): The x position to move to before scrolling. Defaults to the current mouse position.
            y (int, optional): The y position to move to before scrolling. Defaults to the current mouse position.
        """
        if x is not None and y is not None:
            scroll_x, scroll_y = x, y
            self.moveTo(scroll_x, scroll_y)
        elif x is None and y is None:
            scroll_x, scroll_y = self.position()
        else:  # one of x or y is None
            current_x, current_y = self.position()
            scroll_x = x if x is not None else current_x
            scroll_y = y if y is not None else current_y
            self.moveTo(scroll_x, scroll_y)

        self.logger.info(f"scroll(clicks={clicks}) at ({scroll_x}, {scroll_y})")

        # In pyautogui, positive clicks scroll up.
        # The MouseScrollAction uses stepVertical, assuming positive is up.
        request = MouseScrollAction(
            type="mouse:scroll",
            x=PixelLength(type="px", value=scroll_x),
            y=PixelLength(type="px", value=scroll_y),
            stepVertical=clicks,
            stepHorizontal=0
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def write(self, message: str, interval: float = 0.0, _pause: bool = True):
        """
        Types the specified message into the keyboard.
        This is a wrapper for typewrite().

        Args:
            message (str): The message to type.
            interval (float, optional): The interval in seconds between each key press. Defaults to 0.0.
        """
        self.typewrite(message, interval=interval, _pause=_pause)

    def typewrite(self, message: Union[str, List[str]], interval: float = 0.0, _pause: bool = True):
        """
        Types the specified message.

        Args:
            message (str or List[str]): The message to type. If a string, it's typed out.
                                         If a list of strings, each string is typed or pressed as a key.
            interval (float, optional): The interval in seconds between each key press. Defaults to 0.0.
        """
        if isinstance(message, str):
            if interval == 0.0:
                request = KeyboardTypeAction(
                    type="keyboard:type",
                    content=message,
                    treatNewLineAsEnter=True
                )
                coro = self.sandbox.execute_sandbox_action(
                    sandbox_id=self.sandbox_id,
                    data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
                )
                self._run_sync(coro)
                return

            keys_to_press = ['enter' if char == '\n' else char for char in message]
            self.press(keys_to_press, interval=interval, _pause=_pause)

        elif isinstance(message, list):
            self.press(message, interval=interval, _pause=_pause)
        else:
            raise TypeError("message argument must be a string or a list of strings.")

    @overload
    def press(self, keys: str, presses: int = 1, interval: float = 0.0, _pause: bool = True): ...

    @overload
    def press(self, keys: List[str], presses: int = 1, interval: float = 0.0, _pause: bool = True): ...

    def press(self, keys, presses=1, interval=0.0, _pause=True):
        """
        Presses the specified keys.

        Args:
            keys (str or List[str]): The key to press, or a list of keys to press in sequence.
            presses (int, optional): The number of times to press the keys. Defaults to 1.
            interval (float, optional): The interval in seconds between each press. Defaults to 0.0
        """
        if isinstance(keys, str):
            _keys = [keys] * presses
        else:
            _keys = keys * presses

        for i, key in enumerate(_keys):
            request = KeyboardHotkeyAction(
                type="keyboard:hotkey",
                keys=key
            )
            coro = self.sandbox.execute_sandbox_action(
                sandbox_id=self.sandbox_id,
                data=ExecuteSandboxActionDto(action=request, includeScreenShot=False,
                                              includeCursorPosition=False)
            )
            self._run_sync(coro)
            if i < len(_keys) - 1:
                time.sleep(interval)

    def hotkey(self, *args, interval=0.0, _pause=True):
        """
        Presses a hotkey combination.

        Args:
            *args (str): The keys to press.
            interval (Placeholder):
        """
        keys = args
        if len(keys) == 1 and isinstance(keys[0], (list, tuple)):
            keys = keys[0]

        keys_to_press = '+'.join(keys)
        request = KeyboardHotkeyAction(
            type="keyboard:hotkey",
            keys=keys_to_press
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def keyDown(self, key):
        """
        Holds down a key.

        Args:
            key (str): The key to hold down.
        """
        request = KeyDownAction(
            type="key:down",
            key=key
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def keyUp(self, key):
        """
        Releases a key.

        Args:
            key (str): The key to release.
        """
        request = KeyUpAction(
            type="key:up",
            key=key
        )
        coro = self.sandbox.execute_sandbox_action(
            sandbox_id=self.sandbox_id,
            data=ExecuteSandboxActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)
