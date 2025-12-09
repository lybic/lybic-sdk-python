# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
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
Example: Using synchronous Lybic client

This example demonstrates how to use the synchronous Lybic SDK client.
"""
# pylint: disable=wrong-import-position,reimported,invalid-name,f-string-without-interpolation
# Example 1: Basic synchronous client usage
from lybic_sync import LybicSyncClient

# Create a synchronous client (uses environment variables LYBIC_ORG_ID, LYBIC_API_KEY, LYBIC_API_ENDPOINT)
client = LybicSyncClient()

# Or with explicit credentials
from lybic_sync import LybicAuth
auth = LybicAuth(
    org_id="your-org-id",
    api_key="your-api-key",
    endpoint="https://api.lybic.cn"
)
client = LybicSyncClient(auth=auth)

# Use context manager for automatic cleanup
with LybicSyncClient(auth=auth) as client:
    # List sandboxes
    sandboxes = client.sandbox.list()
    print(f"Found {len(sandboxes)} sandboxes")

    # Get organization stats
    stats = client.stats.get()
    print(f"Organization has {stats.sandboxes} sandboxes")

    # List projects
    projects = client.project.list()
    print(f"Found {len(projects)} projects")


# Example 2: Using synchronous PyautoguiSync
from lybic_sync import LybicSyncClient, PyautoguiSync

client = LybicSyncClient()
sandbox_id = "your-sandbox-id"

# Create PyautoguiSync instance
pyautogui = PyautoguiSync(client, sandbox_id)

# Use pyautogui methods
pos = pyautogui.position()
print(f"Current mouse position: {pos}")

pyautogui.moveTo(100, 100)
pyautogui.click()
pyautogui.write("Hello from sync client!")


# Example 3: Using async client with Pyautogui (automatically converts to sync)
from lybic import LybicClient, Pyautogui

async_client = LybicClient()
# Pyautogui will automatically convert async client to sync client internally
pyautogui = Pyautogui(async_client, sandbox_id)

# Use pyautogui methods synchronously
pyautogui.click(100, 100)
pyautogui.write("This works with both async and sync clients!")


# Example 4: Sandbox operations
with LybicSyncClient(auth=auth) as client:
    # Create a sandbox
    sandbox = client.sandbox.create(
        name="my-sandbox",
        shape="standard",
        maxLifeSeconds=3600
    )
    print(f"Created sandbox: {sandbox.id}")

    # Execute an action
    from lybic.action import MouseClickAction, PixelLength
    from lybic.dto import ExecuteSandboxActionDto

    action = MouseClickAction(
        type="mouse:click",
        x=PixelLength(type="px", value=100),
        y=PixelLength(type="px", value=100),
        button=1
    )

    result = client.sandbox.execute_sandbox_action(
        sandbox_id=sandbox.id,
        data=ExecuteSandboxActionDto(
            action=action,
            includeScreenShot=True,
            includeCursorPosition=True
        )
    )
    print(f"Action executed, screenshot available at: {result.screenShot}")

    # Delete the sandbox
    client.sandbox.delete(sandbox.id)
    print(f"Sandbox deleted")


# Example 5: Computer Use tools
with LybicSyncClient(auth=auth) as client:
    # Parse LLM output
    from lybic.dto import ModelType

    llm_output = """
    I will click at position (100, 200) and then type "Hello"
    """

    actions = client.tools.computer_use.parse_llm_output(
        model_type=ModelType.PYAUTOGUI,
        llm_output=llm_output
    )
    print(f"Parsed {len(actions.actions)} actions from LLM output")
