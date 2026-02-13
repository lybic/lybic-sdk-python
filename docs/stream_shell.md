# StreamShell API Documentation

The StreamShell API provides interactive shell session capabilities for Lybic sandboxes. Unlike the v1 `sandbox.execute_process` API, StreamShell supports:

- **Server-Sent Events (SSE)** streaming for real-time output
- **Interactive TTY** sessions
- **Bidirectional communication** with running shells
- **Timeout control** and working directory specification

## Table of Contents

- [Quick Start](#quick-start)
- [API Methods](#api-methods)
- [Data Models](#data-models)
- [Examples](#examples)

## Quick Start

### Async Usage

```python
import asyncio
from lybic import LybicClient, LybicAuth
from lybic.stream_shell import StreamEventType

async def main():
    auth = LybicAuth()
    async with LybicClient(auth=auth) as client:
        # Streaming execution
        async for event in client.stream_shell.create_stream(
            sandbox_id="your-sandbox-id",
            command="echo 'Hello World'",
        ):
            if event.event_type == StreamEventType.STDOUT:
                print(event.data, end="")

asyncio.run(main())
```

### Sync Usage

```python
from lybic_sync import LybicSyncClient, LybicAuth
from lybic.stream_shell import StreamEventType

auth = LybicAuth()
with LybicSyncClient(auth=auth) as client:
    for event in client.stream_shell.create_stream(
        sandbox_id="your-sandbox-id",
        command="ls -la",
    ):
        if event.event_type == StreamEventType.STDOUT:
            print(event.data, end="")
```

## API Methods

### `create_stream()`

Create a streaming shell session that returns real-time output via SSE.

**Parameters:**
- `sandbox_id` (str): The ID of the sandbox
- `command` (str): The command to execute
- `use_tty` (bool, optional): Whether to use a TTY. Default: `False`
- `timeout_seconds` (int, optional): Timeout in seconds (1-86400)
- `working_directory` (str, optional): Working directory for the command
- `tty_rows` (int, optional): Number of TTY rows (if `use_tty` is True)
- `tty_cols` (int, optional): Number of TTY columns (if `use_tty` is True)

**Returns:** `AsyncIterator[StreamEvent]` or `Iterator[StreamEvent]`

**Example:**
```python
async for event in client.stream_shell.create_stream(
    sandbox_id="sandbox-123",
    command="npm install",
    working_directory="/app",
    timeout_seconds=300,
):
    if event.event_type == StreamEventType.STDOUT:
        print(event.data, end="")
```

### `create()`

Create an interactive shell session that can be written to and read from.

**Parameters:** Same as `create_stream()`

**Returns:** `SandboxShellCommandCreateResponseDto` with `sessionId`

**Example:**
```python
response = await client.stream_shell.create(
    sandbox_id="sandbox-123",
    command="bash",
    use_tty=True,
    tty_rows=24,
    tty_cols=80,
)
shell_id = response.sessionId
```

### `write()`

Write input data to an interactive shell session.

**Parameters:**
- `sandbox_id` (str): The ID of the sandbox
- `shell_id` (str): The ID of the shell session
- `data` (str): The input data to write

**Example:**
```python
await client.stream_shell.write(sandbox_id, shell_id, "ls -la\n")
```

### `read()`

Read accumulated output from a shell session.

**Parameters:**
- `sandbox_id` (str): The ID of the sandbox
- `shell_id` (str): The ID of the shell session

**Returns:** `SandboxShellCommandReadResponseDto` with `output` and `isRunning`

**Example:**
```python
read_response = await client.stream_shell.read(sandbox_id, shell_id)
for output in read_response.output:
    if output.oneofKind == "stdout":
        print(output.stdout)
```

### `finish()`

Signal EOF to the shell session (finish writing).

**Parameters:**
- `sandbox_id` (str): The ID of the sandbox
- `shell_id` (str): The ID of the shell session

**Example:**
```python
await client.stream_shell.finish(sandbox_id, shell_id)
```

### `terminate()`

Terminate a shell session.

**Parameters:**
- `sandbox_id` (str): The ID of the sandbox
- `shell_id` (str): The ID of the shell session

**Example:**
```python
await client.stream_shell.terminate(sandbox_id, shell_id)
```

## Data Models

### StreamEvent

Represents a streaming event from shell execution.

**Fields:**
- `event_type` (StreamEventType): The type of event
- `data` (str): The decoded data (base64 is automatically decoded)

### StreamEventType (Enum)

- `STDOUT`: Standard output
- `STDERR`: Standard error
- `WAITING`: Command finished, waiting to exit
- `TIMEOUT`: Timeout occurred
- `END`: Stream ended

### ShellOutput (Union)

Output from a shell session read operation:

- `ShellOutputStdout`: `oneofKind="stdout"`, `stdout: str`
- `ShellOutputStderr`: `oneofKind="stderr"`, `stderr: str`
- `ShellOutputWaiting`: `oneofKind="waiting"`, `waiting: bool`

## Examples

### Example 1: Simple Command Execution

```python
async with LybicClient(auth=auth) as client:
    async for event in client.stream_shell.create_stream(
        sandbox_id="sandbox-123",
        command="python --version",
    ):
        if event.event_type == StreamEventType.STDOUT:
            print(event.data, end="")
        elif event.event_type == StreamEventType.END:
            break
```

### Example 2: Interactive Shell with TTY

```python
async with LybicClient(auth=auth) as client:
    # Create interactive shell
    response = await client.stream_shell.create(
        sandbox_id="sandbox-123",
        command="bash",
        use_tty=True,
        tty_rows=24,
        tty_cols=80,
    )
    shell_id = response.sessionId
    
    # Execute commands
    await client.stream_shell.write(sandbox_id, shell_id, "cd /app\n")
    await client.stream_shell.write(sandbox_id, shell_id, "ls -la\n")
    
    # Read output
    output = await client.stream_shell.read(sandbox_id, shell_id)
    for item in output.output:
        if item.oneofKind == "stdout":
            print(item.stdout)
    
    # Clean up
    await client.stream_shell.finish(sandbox_id, shell_id)
    await client.stream_shell.terminate(sandbox_id, shell_id)
```

### Example 3: Long-Running Command with Timeout

```python
async with LybicClient(auth=auth) as client:
    try:
        async for event in client.stream_shell.create_stream(
            sandbox_id="sandbox-123",
            command="npm install",
            working_directory="/app",
            timeout_seconds=600,  # 10 minutes
        ):
            if event.event_type == StreamEventType.STDOUT:
                print(f"[STDOUT] {event.data}", end="")
            elif event.event_type == StreamEventType.STDERR:
                print(f"[STDERR] {event.data}", end="")
            elif event.event_type == StreamEventType.TIMEOUT:
                print(f"Command timed out: {event.data}")
            elif event.event_type == StreamEventType.END:
                print("Command completed")
                break
    except Exception as e:
        print(f"Error: {e}")
```

## Differences from v1 `execute_process`

| Feature | `execute_process` (v1) | `stream_shell` (v2) |
|---------|------------------------|---------------------|
| Real-time output | ❌ | ✅ (via SSE) |
| Interactive sessions | ❌ | ✅ |
| TTY support | ❌ | ✅ |
| Working directory | ✅ | ✅ |
| Timeout control | ✅ | ✅ |
| Bidirectional I/O | ❌ | ✅ |

## Error Handling

```python
from lybic.exceptions import LybicAPIError

try:
    async for event in client.stream_shell.create_stream(
        sandbox_id="invalid-id",
        command="ls",
    ):
        print(event.data)
except LybicAPIError as e:
    print(f"API Error: {e.message} (code: {e.code})")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## See Also

- [Full Example Script](../examples/stream_shell_example.py)
- [Lybic SDK Documentation](../README.md)
