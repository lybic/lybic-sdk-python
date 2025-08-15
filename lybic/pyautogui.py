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

from lybic import LybicClient, PyautoguiLybic

client = LybicClient()
pyautogui = PyautoguiLybic(client)

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
from typing import overload, Optional, Coroutine

from lybic.lmcp import ComputerUse
from lybic import LybicClient, dto


class PyautoguiLybic:
    """
    PyautoguiLybic implements a calling interface compatible with pyautogui.py through lybic

    Examples:

    LLM_OUTPUT = 'pyautogui.click(x=1443, y=343)'

    from lybic import LybicClient, PyautoguiLybic

    client = LybicClient()

    pyautogui = PyautoguiLybic(client,sandbox_id)

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

    @overload
    def clone(self, sandbox_id: str) -> "PyautoguiLybic": ...

    @overload
    def clone(self) -> "PyautoguiLybic": ...

    def clone(self, sandbox_id: str = None) -> "PyautoguiLybic":
        # Note: The cloned object will have its own background thread.
        if sandbox_id is not None:
            return PyautoguiLybic(self.client, sandbox_id)
        else:
            return PyautoguiLybic(self.client, self.sandbox_id)

    def position(self) -> tuple[int, int]:
        return self.get_mouse_position()

    def get_mouse_position(self) -> tuple[int, int]:
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            data=dto.ComputerUseActionDto(
                action=dto.FinishedAction(type="finished"),
                includeScreenShot=False,
                includeCursorPosition=True
            )
        )
        result = self._run_sync(coro)
        if result.cursorPosition:
            return result.cursorPosition.x, result.cursorPosition.y
        raise ConnectionError("Could not get mouse position")

    def moveTo(self, x, y, duration=0.0, tween=None, logScreenshot=False, _pause=True):
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
        if xOffset is None and yOffset is None:
            return

        current_x, current_y = self.position()
        xOffset = xOffset or 0
        yOffset = yOffset or 0

        new_x = current_x + xOffset
        new_y = current_y + yOffset
        self.moveTo(new_x, new_y, duration, tween, _pause=_pause)

    def click(self, x: Optional[int] = None, y: Optional[int] = None,
              clicks=1, interval=0.0, button='left', duration=0.0, tween=None,
              logScreenshot=None, _pause=True):
        if x is None or y is None:
            x, y = self.position()

        self.logger.info(f"click(x={x}, y={y}, clicks={clicks}, button='{button}')")

        button_map = {'left': 1, 'right': 2, 'middle': 4}
        button_code = button_map.get(button.lower(), 1)

        for i in range(clicks):
            if clicks == 2:
                action = dto.MouseDoubleClickAction(
                    type="mouse:doubleClick",
                    x=dto.PixelLength(type="px", value=x),
                    y=dto.PixelLength(type="px", value=y),
                    button=button_code
                )
            else:
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
        if x is None or y is None:
            x, y = self.position()
        self.click(x, y, clicks=2, interval=interval, button=button, duration=duration, tween=tween, _pause=_pause)

    def write(self, message, interval=0.0, _pause=True):
        request = dto.KeyboardTypeAction(
            type="keyboard:type",
            content=message
        )
        coro = self.computer_use.execute_computer_use_action(
            sandbox_id=self.sandbox_id,
            data=dto.ComputerUseActionDto(action=request, includeScreenShot=False, includeCursorPosition=False)
        )
        self._run_sync(coro)

    def press(self, keys, presses=1, interval=0.0, _pause=True):
        for i in range(presses):
            request = dto.KeyboardHotkeyAction(
                type="keyboard:hotkey",
                keys=keys
            )
            coro = self.computer_use.execute_computer_use_action(
                sandbox_id=self.sandbox_id,
                data=dto.ComputerUseActionDto(action=request, includeScreenShot=False,
                                              includeCursorPosition=False)
            )
            self._run_sync(coro)
            if i < presses - 1:
                time.sleep(interval)

    def hotkey(self, *args, interval=0.0, _pause=True):
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
        self.logger.warning("keyDown is not implemented in Lybic SDK")
        raise NotImplementedError("Lybic API does not support holding a key down.")

    def keyUp(self, key):
        self.logger.warning("keyUp is not implemented in Lybic SDK")
        raise NotImplementedError("Lybic API does not support releasing a key.")
