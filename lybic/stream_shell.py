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

"""stream_shell.py provides the Streaming Shell API for interactive shell sessions."""
import base64
import json
from typing import AsyncIterator, TYPE_CHECKING, Optional

from lybic.dto import (
    StreamEvent,
    StreamEventType,
    SandboxShellCommandStreamCreateRequestDto,
    SandboxShellCommandCreateResponseDto,
    SandboxShellCommandCreateRequestDto,
    SandboxShellCommandWriteRequestDto,
    SandboxShellCommandReadResponseDto,
)

if TYPE_CHECKING:
    from lybic.lybic import LybicClient

# pylint: disable=too-many-locals,protected-access
class StreamShell:
    """Stream Shell API for interactive shell sessions."""

    def __init__(self, client: "LybicClient"):
        self.client = client

    async def create_stream(
        self,
        sandbox_id: str,
        command: str,
        use_tty: bool = False,
        timeout_seconds: Optional[int] = None,
        working_directory: Optional[str] = None,
        tty_rows: Optional[int] = None,
        tty_cols: Optional[int] = None,
    ) -> AsyncIterator[StreamEvent]:
        """
        Create a streaming shell session (SSE).
        
        Args:
            sandbox_id: The ID of the sandbox.
            command: The command to execute in the shell.
            use_tty: Whether to use a TTY for the shell session.
            timeout_seconds: Optional timeout for the shell session in seconds.
            working_directory: Optional working directory for the shell session.
            tty_rows: Number of rows for TTY (if use_tty is true).
            tty_cols: Number of columns for TTY (if use_tty is true).
            
        Yields:
            StreamEvent: Events from the shell execution.
        """
        request = SandboxShellCommandStreamCreateRequestDto(
            command=command,
            useTty=use_tty,
            timeoutSeconds=timeout_seconds,
            workingDirectory=working_directory,
            ttyRows=tty_rows,
            ttyCols=tty_cols,
        )

        self.client.logger.debug(f"Creating streaming shell session for sandbox {sandbox_id}")
        self.client._ensure_client_is_open()
        url = f"{self.client.endpoint}/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell/stream"

        async with self.client.client.stream(
            "POST",
            url,
            json=request.model_dump(exclude_none=True),
            headers=self.client.headers,
            timeout=None,
        ) as response:
            response.raise_for_status()

            async for line in response.aiter_lines():
                if not line:
                    continue

                if line.startswith("data: "):
                    data_str = line[6:]
                    try:
                        event_data = json.loads(data_str)

                        # Parse the event
                        if "stdout" in event_data:
                            decoded = base64.b64decode(event_data["stdout"]).decode("utf-8")
                            yield StreamEvent(event_type=StreamEventType.STDOUT, data=decoded)
                        elif "stderr" in event_data:
                            decoded = base64.b64decode(event_data["stderr"]).decode("utf-8")
                            yield StreamEvent(event_type=StreamEventType.STDERR, data=decoded)
                        elif "waiting" in event_data:
                            yield StreamEvent(event_type=StreamEventType.WAITING, data="")
                        elif "timeout" in event_data:
                            decoded = base64.b64decode(event_data["timeout"]).decode("utf-8")
                            yield StreamEvent(event_type=StreamEventType.TIMEOUT, data=decoded)
                        elif "end" in event_data:
                            yield StreamEvent(event_type=StreamEventType.END, data="")
                            break
                    except (json.JSONDecodeError, KeyError, ValueError) as e:
                        self.client.logger.warning(f"Failed to parse SSE event: {e}")
                        continue

    async def create(
        self,
        sandbox_id: str,
        command: str,
        use_tty: bool = False,
        timeout_seconds:Optional[int] = None,
        working_directory: Optional[str] = None,
        tty_rows: Optional[int] = None,
        tty_cols: Optional[int] = None,
    ) -> SandboxShellCommandCreateResponseDto:
        """
        Create a shell session.
        
        Args:
            sandbox_id: The ID of the sandbox.
            command: The command to execute in the shell.
            use_tty: Whether to use a TTY for the shell session.
            timeout_seconds: Optional timeout for the shell session in seconds.
            working_directory: Optional working directory for the shell session.
            tty_rows: Number of rows for TTY (if use_tty is true).
            tty_cols: Number of columns for TTY (if use_tty is true).
            
        Returns:
            SandboxShellCommandCreateResponseDto: The created session information.
        """
        request = SandboxShellCommandCreateRequestDto(
            command=command,
            useTty=use_tty,
            timeoutSeconds=timeout_seconds,
            workingDirectory=working_directory,
            ttyRows=tty_rows,
            ttyCols=tty_cols,
        )
        self.client.logger.debug(f"Creating shell session for sandbox {sandbox_id}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell",
            json=request.model_dump(exclude_none=True)
        )
        self.client.logger.debug(f"Create shell session response: {response.text}")
        return SandboxShellCommandCreateResponseDto.model_validate_json(response.text)

    async def write(
        self,
        sandbox_id: str,
        shell_id: str,
        data: str,
    ) -> None:
        """
        Write text to a shell session.
        
        Args:
            sandbox_id: The ID of the sandbox.
            shell_id: The ID of the shell session.
            data: The input data to write to the shell session.
        """
        request = SandboxShellCommandWriteRequestDto(data=data)

        self.client.logger.debug(f"Writing to shell session {shell_id} in sandbox {sandbox_id}")
        await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell/{shell_id}",
            json=request.model_dump(exclude_none=True)
        )

    async def finish(
        self,
        sandbox_id: str,
        shell_id: str,
    ) -> None:
        """
        Finish writing to a shell session.
        
        Args:
            sandbox_id: The ID of the sandbox.
            shell_id: The ID of the shell session.
        """
        self.client.logger.debug(f"Finishing shell session {shell_id} in sandbox {sandbox_id}")
        await self.client.request(
            "PUT",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell/{shell_id}/finish"
        )

    async def read(
        self,
        sandbox_id: str,
        shell_id: str,
    ) -> SandboxShellCommandReadResponseDto:
        """
        Read shell output.
        
        Args:
            sandbox_id: The ID of the sandbox.
            shell_id: The ID of the shell session.
            
        Returns:
            SandboxShellCommandReadResponseDto: The output from the shell session.
        """
        self.client.logger.debug(f"Reading shell session {shell_id} in sandbox {sandbox_id}")
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell/{shell_id}/read"
        )
        self.client.logger.debug(f"Read shell session response: {response.text}")
        return SandboxShellCommandReadResponseDto.model_validate_json(response.text)

    async def terminate(
        self,
        sandbox_id: str,
        shell_id: str,
    ) -> None:
        """
        Terminate a shell session.
        
        Args:
            sandbox_id: The ID of the sandbox.
            shell_id: The ID of the shell session.
        """
        self.client.logger.debug(f"Terminating shell session {shell_id} in sandbox {sandbox_id}")
        await self.client.request(
            "DELETE",
            f"/api/orgs/{self.client.org_id}/sandboxes/{sandbox_id}/shell/{shell_id}"
        )
