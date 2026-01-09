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
pyautogui.py implements a synchronous calling interface compatible with pyautogui.py through lybic

from lybic import LybicClient, Pyautogui

# You can use either async or sync client
# With async client (uses synchronous client internally):
client = LybicClient()
pyautogui = Pyautogui(client, 'your-sandbox-id')

# Or with sync client directly:
from lybic_sync import LybicSyncClient
sync_client = LybicSyncClient()
pyautogui = Pyautogui(sync_client, 'your-sandbox-id')

The following pyautogui code remains compatible with Lybic actions:

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
import logging
import re
from typing import overload, Optional, List, Union, TYPE_CHECKING

from lybic.authentication import LybicAuth
from lybic.action import (
    FinishedAction,
    ComputerUseAction,
    MobileUseAction,
)

from lybic.dto import ExecuteSandboxActionDto, ModelType

if TYPE_CHECKING:
    from lybic.lybic import LybicClient


# pylint: disable=unused-argument,invalid-name,logging-fstring-interpolation
class PyautoguiSync:
    """
    Pyautogui implements a calling interface compatible with pyautogui.py through lybic

    Examples:

    LLM_OUTPUT = 'pyautogui.click(x=1443, y=343)'

    from lybic import LybicClient, Pyautogui
    from lybic_sync.lybic_sync import LybicSyncClient

    client = LybicClient() || LybicSyncClient()

    pyautogui = Pyautogui(client,sandbox_id)

    eval(LLM_OUTPUT)
    """
    def __init__(self, client, sandbox_id: str):
        self.logger = logging.getLogger(__name__)

        # Check if client is a sync client
        # pylint: disable=import-outside-toplevel
        from lybic_sync.lybic_sync import LybicSyncClient
        from lybic.lybic import LybicClient

        if isinstance(client, LybicSyncClient):
            # Use sync client directly
            self.client = client
        elif isinstance(client, LybicClient):
            # Convert async client to sync client
            self.logger.info("Converting async LybicClient to synchronous client for Pyautogui")
            self.client = LybicSyncClient(
                auth=LybicAuth(
                    org_id=client.org_id,
                    api_key=client._api_key,
                    endpoint=client.endpoint,
                    extra_headers=client.headers,
                ),
                timeout=client.timeout,
                max_retries=client.max_retries,
            )
        else:
            raise TypeError("client must be either LybicClient or LybicSyncClient")

        self.sandbox = self.client.sandbox
        self.sandbox_id = sandbox_id
        self.mobile_sandbox = self._sandbox_is_mobile()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # The `LybicClient` lifecycle is controlled by the upper layer.
        pass

    def _sandbox_is_mobile(self) -> bool:
        sandbox = self.sandbox.get(self.sandbox_id)
        return sandbox.sandbox.shape.os == "Android"

    @staticmethod
    def parse(content: str) -> str:
        """
        Parses the given text content to extract pyautogui commands.

        Args:
            content (str): The text content to parse.

        Returns:
            str: A string containing the extracted pyautogui commands, each on a new line.
        """
        pattern = r"pyautogui\.[a-zA-Z_]\w*\(.*\)"
        matches = re.findall(pattern, content)
        return "\n".join(matches)

    @overload
    def clone(self, sandbox_id: str) -> "PyautoguiSync":
        ...

    @overload
    def clone(self) -> "PyautoguiSync":
        ...

    def clone(self, sandbox_id: str = None) -> "PyautoguiSync":
        """
        Clones the PyautoguiSync object with a new sandbox ID.

        Args:
            sandbox_id (str, optional): The sandbox ID to clone the object with. If not provided, the original sandbox ID will be used.

        Returns:
            PyautoguiSync: A new PyautoguiSync object with the specified sandbox ID.
        """
        if sandbox_id is not None:
            return PyautoguiSync(self.client, sandbox_id)
        return PyautoguiSync(self.client, self.sandbox_id)

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
        result = self.sandbox.execute_sandbox_action(
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
        if result.cursorPosition:
            return result.cursorPosition.x, result.cursorPosition.y
        raise ConnectionError("Could not get mouse position")

    def _execute_action(self, code):
        actions: List[MobileUseAction] | List[ComputerUseAction]

        if self.mobile_sandbox:
            actions = self.client.tools.mobile_use.parse_llm_output(
                model_type=ModelType.PYAUTOGUI,
                llm_output=code
            ).actions
        else:
            actions = self.client.tools.computer_use.parse_llm_output(
                model_type=ModelType.PYAUTOGUI,
                llm_output=code
            ).actions

        for action in actions:
            self.sandbox.execute_sandbox_action(
                sandbox_id=self.sandbox_id,
                data=ExecuteSandboxActionDto(action=action, includeScreenShot=False, includeCursorPosition=False)
            )

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
        code = f"""```python
        pyautogui.moveTo(x={x}, y={y}, duration={duration}, tween={tween}, logScreenshot={logScreenshot}, _pause={_pause})
        ```"""
        self._execute_action(code)

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
        code = f"""```python
        pyautogui.move(xOffset={xOffset}, yOffset={yOffset}, duration={duration}, tween={tween}, _pause={_pause})
        ```"""
        self._execute_action(code)

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
        code = f"""```python
        pyautogui.click(x={x}, y={y}, clicks={clicks}, interval={interval}, button='{button}', duration={duration}, tween={tween}, logScreenshot={logScreenshot}, _pause={_pause})
        ```"""
        self._execute_action(code)

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
                    interval: float = 0.0, button: str = 'left', duration: float = 0.0, tween=None,
                    _pause: bool = True):
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
        code = f"""```python
        pyautogui.dragTo(x={x}, y={y}, duration={duration}, button='{button}', _pause={_pause})
        ```"""
        self._execute_action(code)

    def scroll(self, clicks: int, x: Optional[int] = None, y: Optional[int] = None, _pause: bool = True):
        """
        Scrolls the mouse wheel.
        Args:
            clicks (int): The amount of scrolling to perform. Positive values scroll up, negative values scroll down.
            x (int, optional): The x position to move to before scrolling. Defaults to the current mouse position.
            y (int, optional): The y position to move to before scrolling. Defaults to the current mouse position.
        """
        if x is None or y is None:
            x, y = self.position()

        code = f"""```python
        pyautogui.scroll(clicks={clicks}, x={x}, y={y}, _pause={_pause})
        ```"""
        self._execute_action(code)

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
        code = f"""```python
        pyautogui.typewrite(message={repr(message)}, interval={interval}, _pause={_pause})
        ```"""
        self._execute_action(code)

    @overload
    def press(self, keys: str, presses: int = 1, interval: float = 0.0, _pause: bool = True):
        ...

    @overload
    def press(self, keys: List[str], presses: int = 1, interval: float = 0.0, _pause: bool = True):
        ...

    def press(self, keys, presses=1, interval=0.0, _pause=True):
        """
        Presses the specified keys.

        Args:
            keys (str or List[str]): The key to press, or a list of keys to press in sequence.
            presses (int, optional): The number of times to press the keys. Defaults to 1.
            interval (float, optional): The interval in seconds between each press. Defaults to 0.0
        """
        code = f"""```python
        pyautogui.press(keys={repr(keys)}, presses={presses}, interval={interval}, _pause={_pause})
        ```"""
        self._execute_action(code)

    def hotkey(self, *args, interval=0.0, _pause=True):
        """
        Presses a hotkey combination.

        Args:
            *args (str): The keys to press.
            interval (float, optional): The interval in seconds between each press. Defaults to 0.0.
        """
        code = f"""```python
        pyautogui.hotkey({', '.join(repr(key) for key in args)}, interval={interval}, _pause={_pause})
        ```"""
        self._execute_action(code)

    def keyDown(self, key):
        """
        Holds down a key.

        Args:
            key (str): The key to hold down.
        """
        code = f"""```python
        pyautogui.keyDown(key={repr(key)})
        ```"""
        self._execute_action(code)

    def keyUp(self, key):
        """
        Releases a key.

        Args:
            key (str): The key to release.
        """
        code = f"""```python
        pyautogui.keyUp(key={repr(key)})
        ```"""
        self._execute_action(code)

    # pylint: disable=missing-function-docstring
    def close(self):
        pass
