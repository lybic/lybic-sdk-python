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
pyautogui.move(None, 10)
pyautogui.doubleClick()
pyautogui.moveTo(500, 500)
pyautogui.write('Hello world!')
pyautogui.press('esc')
pyautogui.keyDown('shift')
pyautogui.keyUp('shift')
pyautogui.hotkey('ctrl', 'c')
"""
import asyncio
import logging
import threading
import time
from typing import overload, Optional, Coroutine, List

from lybic import dto
from lybic.lybic import LybicClient
from lybic.mcp import ComputerUse

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
        self.client = client
        self.computer_use = ComputerUse(client)
        self.sandbox_id = sandbox_id
        self.logger = logging.getLogger(__name__)

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
            return Pyautogui(self.client, sandbox_id)
        return Pyautogui(self.client, self.sandbox_id)

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
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            # An action is required to obtain the mouse cursor and screenshot information.
            #
            # The `FinishedAction` , however, does not involve any action operations, is idempotent,
            # and offers the highest performance.
            data=dto.ComputerUseActionDto(
                action=dto.FinishedAction(type="finished"),
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
        request = dto.MouseMoveAction(
            type="mouse:move",
            x=dto.PixelLength(type="px", value=x),
            y=dto.PixelLength(type="px", value=y),
        )
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            data=dto.ComputerUseActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
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
            action = dto.MouseDoubleClickAction(
                type="mouse:doubleClick",
                x=dto.PixelLength(type="px", value=x),
                y=dto.PixelLength(type="px", value=y),
                button=button_code
            )
            coro = self.computer_use.execute_computer_use_action(
                sandbox_id=self.sandbox_id,
                data=dto.ComputerUseActionDto(action=action, includeScreenShot=False,
                                              includeCursorPosition=False)
            )
            self._run_sync(coro)
        else:
            for i in range(clicks):
                action = dto.MouseClickAction(
                    type="mouse:click",
                    x=dto.PixelLength(type="px", value=x),
                    y=dto.PixelLength(type="px", value=y),
                    button=button_code
                )

                coro = self.computer_use.execute_computer_use_action(
                    sandbox_id=self.sandbox_id,
                    data=dto.ComputerUseActionDto(action=action, includeScreenShot=False,
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

    def write(self, message, interval=0.0, _pause=True):
        """
        Types the specified message into the keyboard.

        Args:
            message (str): The message to type.
            interval (Placeholder):
        """
        request = dto.KeyboardTypeAction(
            type="keyboard:type",
            content=message
        )
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            data=dto.ComputerUseActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

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
            request = dto.KeyboardHotkeyAction(
                type="keyboard:hotkey",
                keys=key
            )
            coro = self.computer_use.execute_computer_use_action(
                sandbox_id=self.sandbox_id,
                data=dto.ComputerUseActionDto(action=request, includeScreenShot=False,
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
        keys_to_press = '+'.join(args)
        request = dto.KeyboardHotkeyAction(
            type="keyboard:hotkey",
            keys=keys_to_press
        )
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            data=dto.ComputerUseActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def keyDown(self, key):
        """
        Holds down a key. (not implemented)

        Args:
            key (str): The key to hold down.
        """
        self.logger.warning("keyDown is not implemented in Lybic SDK")
        raise NotImplementedError("Lybic API does not support holding a key down.")

    def keyUp(self, key):
        """
        Releases a key. (not implemented)

        Args:
            key (str): The key to release.
        """
        self.logger.warning("keyUp is not implemented in Lybic SDK")
        raise NotImplementedError("Lybic API does not support releasing a key.")
