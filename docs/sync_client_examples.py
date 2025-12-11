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

The synchronous client (lybic_sync) provides the SAME API interface as the async client (lybic),
but without requiring async/await syntax. This makes it ideal for:
- Simple scripts and automation
- Jupyter notebooks
- Interactive Python shells
- Legacy codebases not using async/await

Key differences from async client:
1. Import from lybic_sync instead of lybic
2. No async/await keywords needed
3. Direct function calls instead of coroutines
"""
# pylint: disable=pointless-string-statement,wrong-import-position,reimported,invalid-name,f-string-without-interpolation,wrong-import-order,ungrouped-imports

# =============================================================================
# Example 1: Basic synchronous client usage
# =============================================================================
from lybic_sync import LybicSyncClient, LybicAuth

# Create a synchronous client (uses environment variables LYBIC_ORG_ID, LYBIC_API_KEY, LYBIC_API_ENDPOINT)
client = LybicSyncClient()

# Or with explicit credentials
auth = LybicAuth(
    org_id="your-org-id",
    api_key="your-api-key",
    endpoint="https://api.lybic.cn"
)
client = LybicSyncClient(auth=auth)

# Best practice: Use context manager for automatic cleanup
with LybicSyncClient(auth=auth) as client:
    # List sandboxes - no await needed!
    sandboxes = client.sandbox.list()
    print(f"Found {len(sandboxes)} sandboxes")

    # Get organization stats
    stats = client.stats.get()
    print(f"Organization has {stats.sandboxes} sandboxes")

    # List projects
    projects = client.project.list()
    print(f"Found {len(projects)} projects")


# =============================================================================
# Example 2: Using synchronous PyautoguiSync
# =============================================================================
from lybic_sync import LybicSyncClient, PyautoguiSync

client = LybicSyncClient()
sandbox_id = "your-sandbox-id"

# Create PyautoguiSync instance - mirrors pyautogui API exactly
pyautogui = PyautoguiSync(client, sandbox_id)

# Use pyautogui methods - all synchronous!
pos = pyautogui.position()
print(f"Current mouse position: {pos}")

pyautogui.moveTo(100, 100)
pyautogui.click()
pyautogui.write("Hello from sync client!")

# Don't forget to clean up
pyautogui.close()
client.close()


# =============================================================================
# Example 3: PyautoguiSync with context manager (recommended)
# =============================================================================
from lybic_sync import LybicSyncClient, PyautoguiSync

with LybicSyncClient() as client:
    sandbox_id = "your-sandbox-id"

    # Context manager automatically handles cleanup
    with PyautoguiSync(client, sandbox_id) as pyautogui:
        # Execute pyautogui commands
        pyautogui.click(100, 100)
        pyautogui.write("Context manager handles cleanup!")
        pyautogui.press("enter")


# =============================================================================
# Example 4: Comparison - Async vs Sync
# =============================================================================
# This shows the SAME API, different invocation patterns

# ASYNC VERSION (lybic)
"""
import asyncio
from lybic import LybicClient, Pyautogui

async def async_example():
    async with LybicClient() as client:
        sandbox_id = "your-sandbox-id"
        
        # Note: Pyautogui methods are sync even with async client
        with Pyautogui(client, sandbox_id) as pyautogui:
            pyautogui.click(100, 100)
            pyautogui.write("Using async client")

asyncio.run(async_example())
"""

# SYNC VERSION (lybic_sync) - No asyncio needed!
from lybic_sync import LybicSyncClient, PyautoguiSync

with LybicSyncClient() as client:
    sandbox_id = "your-sandbox-id"

    with PyautoguiSync(client, sandbox_id) as pyautogui:
        pyautogui.click(100, 100)
        pyautogui.write("Using sync client - simpler!")


# =============================================================================
# Example 5: Sandbox operations
# =============================================================================
from lybic_sync import LybicSyncClient, LybicAuth
from lybic.action import MouseClickAction, PixelLength
from lybic.dto import ExecuteSandboxActionDto

auth = LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

with LybicSyncClient(auth=auth) as client:
    # Create a sandbox - no await!
    sandbox = client.sandbox.create(
        name="my-sandbox",
        shape="standard",
        maxLifeSeconds=3600
    )
    print(f"Created sandbox: {sandbox.sandbox.id}")

    # Get sandbox details
    details = client.sandbox.get(sandbox.sandbox.id)
    print(f"Sandbox details: {details}")

    # Take a screenshot
    screenshot_url, image, webp_base64 = client.sandbox.get_screenshot(sandbox.sandbox.id)
    print(f"Screenshot URL: {screenshot_url}")
    # image.show()  # Display with PIL

    # Execute an action
    action = MouseClickAction(
        type="mouse:click",
        x=PixelLength(type="px", value=100),
        y=PixelLength(type="px", value=100),
        button=1
    )

    result = client.sandbox.execute_sandbox_action(
        sandbox_id=sandbox.sandbox.id,
        data=ExecuteSandboxActionDto(
            action=action,
            includeScreenShot=True,
            includeCursorPosition=True
        )
    )
    print(f"Action executed, screenshot available at: {result.screenShot}")

    # Extend sandbox lifetime
    client.sandbox.extend_life(sandbox.sandbox.id, seconds=1800)  # Extend by 30 min
    print("Sandbox lifetime extended")

    # Delete the sandbox
    client.sandbox.delete(sandbox.sandbox.id)
    print("Sandbox deleted")


# =============================================================================
# Example 6: Computer Use tools - Parse LLM output
# =============================================================================
from lybic_sync import LybicSyncClient, LybicAuth

auth = LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

with LybicSyncClient(auth=auth) as client:
    # Parse LLM output from ui-tars model
    llm_output = """
    Thought: I need to click the submit button
    Action: click(point='<point>213 257</point>')
    """

    # Parse the output - no await!
    actions = client.tools.computer_use.parse_llm_output(
        model_type="ui-tars",
        llm_output=llm_output
    )
    print(f"Parsed {len(actions.actions)} actions from LLM output")

    # Execute the parsed actions on a sandbox
    if actions.actions:
        sandbox_id = "SBX-xxxx"
        for action in actions.actions:
            result = client.sandbox.execute_sandbox_action(
                sandbox_id=sandbox_id,
                action=action
            )
            print(f"Executed action: {action.type}")


# =============================================================================
# Example 7: Project management
# =============================================================================
from lybic_sync import LybicSyncClient, LybicAuth
from lybic import dto

auth = LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

with LybicSyncClient(auth=auth) as client:
    # List all projects
    projects = client.project.list()
    print(f"Total projects: {len(projects)}")

    for project in projects:
        print(f"  - {project.name} ({project.id})")

    # Create a new project
    new_project = client.project.create(
        data=dto.CreateProjectDto(name="My New Project")
    )
    print(f"Created project: {new_project.id}")

    # Delete a project (if needed)
    # client.project.delete(new_project.id)


# =============================================================================
# Example 8: File transfer operations
# =============================================================================
from lybic_sync import LybicSyncClient, LybicAuth
from lybic.dto import (
    SandboxFileCopyRequestDto,
    FileCopyItem,
    SandboxFileLocation,
    HttpGetLocation,
    HttpPutLocation
)

auth = LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

with LybicSyncClient(auth=auth) as client:
    sandbox_id = "SBX-xxxx"

    # Download file from URL to sandbox
    response = client.sandbox.copy_files(
        sandbox_id,
        SandboxFileCopyRequestDto(files=[
            FileCopyItem(
                src=HttpGetLocation(url="https://example.com/input.txt"),
                dest=SandboxFileLocation(path="/home/agent/input.txt")
            )
        ])
    )
    print(f"File copy result: {response}")

    # Upload file from sandbox to URL
    response = client.sandbox.copy_files(
        sandbox_id,
        SandboxFileCopyRequestDto(files=[
            FileCopyItem(
                src=SandboxFileLocation(path="/home/agent/output.txt"),
                dest=HttpPutLocation(url="https://storage.example.com/output.txt")
            )
        ])
    )
    print(f"File upload result: {response}")


# =============================================================================
# Example 9: Process execution in sandbox
# =============================================================================
import base64
from lybic_sync import LybicSyncClient, LybicAuth
from lybic.dto import SandboxProcessRequestDto

auth = LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx")

with LybicSyncClient(auth=auth) as client:
    sandbox_id = "SBX-xxxx"

    # Execute a simple command
    result = client.sandbox.execute_process(
        sandbox_id,
        executable="/bin/echo",
        args=["Hello", "World"]
    )

    stdout = base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')
    print(f"Exit code: {result.exitCode}")
    print(f"Output: {stdout}")

    # Execute Python script with stdin
    stdin_data = base64.b64encode(b"print('Hello from Python')\n").decode()
    result = client.sandbox.execute_process(
        sandbox_id,
        data=SandboxProcessRequestDto(
            executable="/usr/bin/python3",
            args=["-c", "import sys; exec(sys.stdin.read())"],
            workingDirectory="/home/agent",
            stdinBase64=stdin_data
        )
    )

    stdout = base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')
    print(f"Python output: {stdout}")


# =============================================================================
# Summary: Key Differences Between Async and Sync Clients
# =============================================================================
"""
ASYNC CLIENT (lybic):
--------------------
from lybic import LybicClient

async def main():
    async with LybicClient() as client:
        result = await client.sandbox.list()  # Need await
        
asyncio.run(main())

- Requires async/await syntax
- Best for high concurrency scenarios
- Integrates with async frameworks (FastAPI, etc.)
- More complex but more powerful


SYNC CLIENT (lybic_sync):
--------------------------
from lybic_sync import LybicSyncClient

with LybicSyncClient() as client:
    result = client.sandbox.list()  # No await!

- Simple, straightforward syntax
- No async/await needed
- Perfect for scripts, notebooks, simple automation
- Easier to understand and debug


IDENTICAL API:
--------------
Both clients expose the SAME methods with the SAME signatures:
- client.sandbox.list()
- client.sandbox.create()
- client.sandbox.get()
- client.project.list()
- client.stats.get()
- client.tools.computer_use.parse_llm_output()
- etc.

The only difference is async methods need 'await', sync methods don't!


WHEN TO USE WHICH:
------------------
Use SYNC (lybic_sync) when:
✓ Writing simple scripts
✓ Working in Jupyter notebooks
✓ Learning or prototyping
✓ You don't need high concurrency

Use ASYNC (lybic) when:
✓ Managing many sandboxes simultaneously
✓ Building web applications (FastAPI, aiohttp)
✓ Integrating with other async libraries
✓ You need maximum I/O performance
"""
