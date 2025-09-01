<p align="center">
  <a href="https://lybic.ai/">
    <img src="https://avatars.githubusercontent.com/lybic" alt="Lybic Logo" width="120" height="120">
  </a>
</p>

<h1 align="center">Lybic SDK for Python</h1>

<p align="center">
  <a href="https://pypi.org/project/lybic/"><img alt="PyPI" src="https://img.shields.io/pypi/v/lybic"></a>
  <a href="https://github.com/lybic/lybic-sdk-python/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/pypi/l/lybic"></a>
  <a href="https://lybic.ai/docs"><img alt="Documentation" src="https://img.shields.io/badge/documentation-Lybic-orange"></a>
  <a href="https://github.com/lybic/lybic-sdk-python/actions/workflows/pylint.yml"><img alt="Pylint" src="https://github.com/lybic/lybic-sdk-python/actions/workflows/pylint.yml/badge.svg"></a>
</p>

## Table of Contents

- [How It Works](#how-it-works)
- [✨ Why Lybic?](#-why-lybic)
- [🚀 Getting Started](#-getting-started)
  - [1. Installation & Setup](#1-installation--setup)
  - [2. Core Workflow](#2-core-workflow)
  - [3. Debug Request](#3-debug-request)
  - [4. Exception Handling](#4-exception-handling)
- [🌒 Adapt LLM output pyautogui format](#-adapt-llm-output-pyautogui-format)
- [📔 Examples](#-examples)
- [📚 Full Documentation & API Reference](#-full-documentation--api-reference)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)

Developing, testing, and deploying GUI-based AI agents is complex. Developers waste precious time wrestling with cloud instances, VNC servers, and environment configurations instead of focusing on what matters: building intelligent agents.

**Lybic is the infrastructure layer for your GUI agents.**

**Lybic** (/ˈlaɪbɪk/) provides a robust, on-demand infrastructure platform designed specifically for the AI agent development lifecycle. This SDK for Python is your command center for programmatically controlling the entire Lybic ecosystem, empowering you to build, test, and scale your agents with unprecedented speed and simplicity.

## How It Works

The Lybic ecosystem is designed for clarity and control. Your code, powered by the Lybic SDK, interacts with the Lybic Cloud Platform to manage your resources and run your agents in secure, isolated GUI sandboxes.

```mermaid
graph TD
    A[Your Agent Code] --> B(Lybic Python SDK);
    B -- Manages --> C{Projects, Members, Secrets};
    B -- Controls --> D[GUI Sandbox];
    C -- Organizes & Secures --> D;
    E[Lybic Cloud Platform] -- Hosts & Provides --> D;
    B -- API Calls --> E;
```

## ✨ Why Lybic?

Lybic is a complete ecosystem designed to eliminate infrastructure friction and accelerate your agent development workflow.

#### 🚀 Focus on Your Agent, Not Infrastructure
Forget about managing virtual machines, display drivers, and remote desktop software. Lybic provides clean, on-demand GUI sandboxes in the cloud. Spin up a fresh environment in seconds and dedicate your time to your agent's core logic.

#### 🔐 Securely Manage Your Secrets
Stop hardcoding API keys and other sensitive credentials. Lybic includes built-in **Secret Management** at the project level. Store your secrets securely in our vault and access them programmatically from your agents, without ever exposing them in your codebase.

#### 👥 Built for Teams, Ready for Scale
Organize your work with **Projects** and manage team access with fine-grained **Member Roles**. Whether you're a solo developer or part of a large team, Lybic provides the structure and security you need to collaborate and scale effectively.

#### 🤖 Observe and Interact in Real-Time
Every GUI sandbox includes a live, accessible desktop stream. This allows you to monitor your agent's actions in real-time for debugging, or to step in and provide guidance, making it perfect for developing complex tasks and implementing human-in-the-loop workflows.

## 🚀 Getting Started

### 1. Installation & Setup

Getting started is simple. First, install the package from PyPI:

```bash
pip install lybic
```

Then, initialize the client in your Python application. For better security, we recommend using environment variables (`LYBIC_ORG_ID`, `LYBIC_API_KEY`).

```python
import asyncio
from lybic import LybicClient

# The LybicClient automatically picks up credentials from your environment
# def __init__(self,
#             org_id: str = os.getenv("LYBIC_ORG_ID"),
#             api_key: str = os.getenv("LYBIC_API_KEY"),
#             endpoint: str = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.cn"),
#             timeout: int = 10,
#             max_retries: int = 3,
#             extra_headers: dict | None = None) -> None
async def main():
    # Initialize with environment variables
    async with LybicClient() as client:
        pass

    # Or, initialize with explicit credentials
    async with LybicClient(
        org_id="your_org_id", # Lybic organization ID
        api_key="your_api_key", # Lybic API key
        endpoint="https://api.lybic.cn", # Lybic API endpoint
        timeout=10, # Timeout for API requests
        max_retries=3, # Maximum number of request retries
        extra_headers={"User-Agent": "MyAgent/1.0"}, # Custom headers
    ) as client:
        pass

if __name__=='__main__':
    asyncio.run(main())
```

Then, you can start using the `client`.

```python
import asyncio
from lybic import LybicClient, Sandbox

async def main():
    async with LybicClient() as client:
        sandbox = Sandbox(client)
        new_sandbox = await sandbox.create(name="my-sandbox")
        print(new_sandbox)

if __name__ == '__main__':
    asyncio.run(main())
```

Completed, you're ready to start building your agent!

### 2. Core Workflow

With the client initialized, the typical workflow follows these logical steps:

1. **Register(Or be invited into) an Organization**: Lybic allows you to register a new organization to manage your projects and resources.

2. **Create a `Project`**: Projects are the primary way to organize your work. They act as containers for your sandboxes, team members, and secrets.

3. **Launch a `Sandbox`**: Within a project, you can launch a GUI sandbox. This is your agent's secure, cloud-based home.

4. **Automate and Interact**: Once the sandbox is running, your agent can begin its work. The SDK provides all the necessary tools to interact with the sandbox, from executing commands to capturing screenshots.

### 3. Debug Request

You can set logging level to debug request.

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('lybic')
```

### 4. Exception Handling

To ensure that each method in the SDK has **valid and definite** return content, we **DO NOT** handle any errors for 
exception requests.

For the robustness of the program code, all exceptions need to be handled by the user themselves.

Where will the exception occur?

1. init LybicClient()
  
   If you do not pass in a valid `org_id` and `endpoint`, an exception will occur.

2. call all `http` and `mcp` methods

   If the request fails(HTTPCode is 4xx or 5xx, or the request timeout), an exception will occur.

How to handle exceptions?

you can catch exceptions in the `try` block

```python
import asyncio
from lybic import LybicClient, Sandbox

async def main():
    # Use async with to ensure the client is properly managed.
    async with LybicClient() as client:
        sandbox = Sandbox(client)
        try:
            # `await` the asynchronous method call inside the async function.
            preview_result = await sandbox.preview('sandbox_id')
            print(preview_result)
        except Exception as e:
            # Handle potential exceptions from the API call.
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## 🌒 Adapt LLM output pyautogui format

To facilitate the execution of GUI automation scripts generated by Large Language Models (LLMs), which are often trained using the popular `pyautogui` library, the Lybic SDK provides a `Pyautogui` compatibility class. This class mirrors the `pyautogui` interface, allowing you to execute LLM-generated code with minimal changes.

### Usage

First, initialize the `LybicClient` and then create a `Pyautogui` instance, binding it to a specific sandbox. You can then use this instance as if it were the `pyautogui` module.

```python
import asyncio
from lybic import LybicClient, Pyautogui

sandbox_id = "your_sandbox_id"

client = LybicClient()
# Create a Pyautogui instance
pyautogui = Pyautogui(client, sandbox_id)

# Now you can execute pyautogui-style commands
# For example, if an LLM outputs the following string:
llm_output = "pyautogui.moveTo(100, 150)"

# You can execute it like this:
# Warning: Using eval() on untrusted input is a security risk.
# Always sanitize and validate LLM output.
eval(llm_output)

# Or call methods directly
pyautogui.click(x=200, y=200)
pyautogui.write("Hello from Lybic!")
pyautogui.press("enter")

# You need to manually manage `LybicClient` object lifecycles
pyautogui.close()
asyncio.run(client.close())
```

If you want to use automatic context management for `Pyautogui`, you can use the `with` statement:

```python
import asyncio
from lybic import LybicClient, Pyautogui

client = LybicClient()
sandbox_id = "your_sandbox_id"

with Pyautogui(client, sandbox_id) as pyautogui:
    # Now you can execute pyautogui-style commands
    # For example, if an LLM outputs the following string:
    llm_output = "pyautogui.moveTo(100, 150)"
    # You can execute it like this:
    # Warning: Using eval() on untrusted input is a security risk.
    # Always sanitize and validate LLM output.
    eval(llm_output)
    # Or call methods directly
    pyautogui.click(x=200, y=200)
    pyautogui.write("Hello from Lybic!")
    pyautogui.press("enter")
    
asyncio.run(client.close())
```

Special scenario: If you need to run asynchronously:

```python
import asyncio
from lybic import LybicClient, Pyautogui

async def main():
    async with LybicClient() as client:
        # Assume you have a sandbox
        sandbox_id = "your_sandbox_id"

        # Create a Pyautogui instance
        with Pyautogui(client, sandbox_id) as pyautogui:
            # Now you can execute pyautogui-style commands
            # For example, if an LLM outputs the following string:
            llm_output = "pyautogui.moveTo(100, 150)"
    
            # You can execute it like this:
            # Warning: Using eval() on untrusted input is a security risk.
            # Always sanitize and validate LLM output.
            eval(llm_output)
    
            # Or call methods directly
            pyautogui.click(x=200, y=200)
            pyautogui.write("Hello from Lybic!")
            pyautogui.press("enter")

if __name__ == "__main__":
    asyncio.run(main())
```

### Supported Functions

The `lybic.Pyautogui` class supports a subset of the most common `pyautogui` functions.

| Function | Supported | Notes |
| :--- | :---: | :--- |
| `position()` | ✅ | |
| `moveTo()` | ✅ | |
| `move()` | ✅ | |
| `click()` | ✅ | |
| `doubleClick()` | ✅ | |
| `write()` | ✅ | |
| `press()` | ✅ | Supports single key and list of keys. |
| `hotkey()` | ✅ | |
| `keyDown()` | ❌ | Not supported by Lybic API. |
| `keyUp()` | ❌ | Not supported by Lybic API. |

## 📔 Examples:

Please read our [SDK example](docs/example.md).

If you are using MCP, you can read our [MCP Documentation](docs/mcp.md).

## 📚 Full Documentation & API Reference

This README provides a high-level overview of Lybic's capabilities. For detailed, up-to-date code examples, tutorials, and a complete API reference, please visit our **[official documentation site](https://lybic.ai/docs)**.

## 🤝 Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](https://github.com/lybic/lybic-sdk-python/blob/master/CONTRIBUTING.md) for more details on how to get involved.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/lybic/lybic-sdk-python/blob/master/LICENSE) file for details.
