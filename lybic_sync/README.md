# Lybic Sync Client

Synchronous client support for the Lybic SDK.

## Overview

The `lybic_sync` package provides synchronous versions of all Lybic SDK APIs, making it suitable for scenarios where async/await patterns are not appropriate.

## Features

- **Synchronous API** - All API calls are synchronous, no async/await required
- **Reuses shared modules** - Uses the same DTO, action, and authentication modules as the async client
- **Compatible with async client** - Can seamlessly work alongside async code
- **Drop-in replacement** - Similar API structure to the async client

## Installation

The synchronous client is included in the main `lybic` package:

```bash
pip install lybic
```

## Quick Start

```python
from lybic_sync import LybicSyncClient

# Create a synchronous client
client = LybicSyncClient()

# List sandboxes
sandboxes = client.sandbox.list()

# Get organization stats
stats = client.stats.get()
```

## Usage with Context Manager

```python
from lybic_sync import LybicSyncClient, LybicAuth

auth = LybicAuth(
    org_id="your-org-id",
    api_key="your-api-key"
)

with LybicSyncClient(auth=auth) as client:
    sandboxes = client.sandbox.list()
    stats = client.stats.get()
```

## Using PyautoguiSync

```python
from lybic_sync import LybicSyncClient, PyautoguiSync

client = LybicSyncClient()
pyautogui = PyautoguiSync(client, "sandbox-id")

# Use pyautogui methods synchronously
pyautogui.moveTo(100, 100)
pyautogui.click()
pyautogui.write("Hello!")
```

## Using Pyautogui with Both Async and Sync Clients

The `lybic.Pyautogui` class now automatically uses a synchronous client internally, which means it works efficiently with both async and sync clients:

```python
# With async client (automatically converts to sync internally)
from lybic import LybicClient, Pyautogui

async_client = LybicClient()
pyautogui = Pyautogui(async_client, "sandbox-id")
pyautogui.click()  # Works synchronously

# With sync client directly
from lybic_sync import LybicSyncClient
from lybic import Pyautogui

sync_client = LybicSyncClient()
pyautogui = Pyautogui(sync_client, "sandbox-id")
pyautogui.click()  # Works synchronously
```

## Available Components

- **LybicSyncClient** - Main synchronous client
- **SandboxSync** - Synchronous sandbox operations
- **ProjectSync** - Synchronous project management
- **McpSync** - Synchronous MCP operations
- **StatsSync** - Synchronous organization statistics
- **ToolsSync** - Synchronous tool operations
  - **ComputerUseSync** - Computer use tools
  - **MobileUseSync** - Mobile use tools
- **PyautoguiSync** - Synchronous pyautogui interface

## Differences from Async Client

The synchronous client has nearly identical API to the async client, with these differences:

1. No `async`/`await` keywords
2. No `call_tool_async` method in MCP (as it requires async operations)
3. Uses `httpx.Client` instead of `httpx.AsyncClient`
4. No need for event loops or async context managers

## Example: Sandbox Operations

```python
from lybic_sync import LybicSyncClient
from lybic.action import MouseClickAction, PixelLength
from lybic.dto import ExecuteSandboxActionDto

client = LybicSyncClient()

# Create sandbox
sandbox = client.sandbox.create(
    name="my-sandbox",
    shape="standard"
)

# Execute action
action = MouseClickAction(
    type="mouse:click",
    x=PixelLength(type="px", value=100),
    y=PixelLength(type="px", value=100),
    button=1
)

result = client.sandbox.execute_sandbox_action(
    sandbox_id=sandbox.id,
    data=ExecuteSandboxActionDto(action=action)
)

# Delete sandbox
client.sandbox.delete(sandbox.id)
```

## When to Use Sync vs Async

**Use Synchronous Client When:**
- Working in non-async code
- Building CLI tools
- Scripting and automation
- Integrating with synchronous frameworks
- Simpler, more straightforward code flow

**Use Asynchronous Client When:**
- Building async web applications
- Need to handle many concurrent operations
- Working with other async libraries
- Performance optimization for I/O-bound operations

## Migration from Async Client

Migrating from async to sync is straightforward:

```python
# Before (async)
from lybic import LybicClient

async def main():
    client = LybicClient()
    sandboxes = await client.sandbox.list()

# After (sync)
from lybic_sync import LybicSyncClient

def main():
    client = LybicSyncClient()
    sandboxes = client.sandbox.list()
```

## See Also

- [Main Lybic SDK Documentation](../README.md)
- [API Reference](https://docs.lybic.ai/)
- [Examples](../docs/sync_client_examples.py)
