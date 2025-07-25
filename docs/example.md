## examples

```python
from lybic import  LybicClient

client = LybicClient(
    org_id="ORG-xxxx",
    api_key="lysk-xxxxxxxxxxx",
    endpoint="https://api.lybic.cn/",
)
```

### Class Stats

`Stats` is a class for describing the stats of the organization.

1. Get the stats of the organization

    such as number of members, computers, etc.

    method: `get()`
    - args: None
    - return: class dto.StatsResponseDto

    ```python
    from lybic import Stats
    
    stats = Stats(client)
    print(stats.get())
    ```
    
    It will out put something like this:

    ```
    mcpServers=3 sandboxes=8 projects=4
    ```

### Class Project

`Project` is a class for describing the project and used to manage the sandbox of the project.

1. List all projects

   method: `list()`
   - args: None
   - return: class dto.ProjectListResponseDto

   ```python
   from lybic import Project

   project = Project(client)
   list_result = project.list()
   ```

   The returned is a traversable data model list[dto.ProjectResponseDto]

   ```python
   for project in list_result:
       print(project)
   ```
   
   It will out put something like this:(Sort by `createdAt`)
   
   ```
   id='PRJ-xxxx' name='test_project' createdAt='2025-07-10T08:03:36.375Z' defaultProject=False
   id='PRJ-xxxx' name='Default Project' createdAt='2025-07-08T16:42:30.226Z' defaultProject=True
   ```

2. Create a project
   
   method: `create(data: dto.CreateMcpServerDto)`
   - args: class dto.CreateProjectDto
     - *name: str project name
   - return: class dto.SingleProjectResponseDto

   ```python
   from lybic import dto
   from lybic import Project
   
   project = Project(client)
   print(project.create(dto.CreateProjectDto(name="test_project"))) 
   ```
   
   It will out put something like this:

   ```
   id='PRJ-xxxx' name='test_project' createdAt='2025-07-10T08:03:36.375Z' defaultProject=False
   ```

3. Delete a project

   method: `delete(project_id: str)`
   - args: 
     - *project_id: str ID of the project to delete
   - return: None(If No http error)

   ```python
   from lybic import Project
   
   project = Project(client)
   project.delete(project_id="PRJ-xxxx") 
   ```

### Class MCP

`MCP` is a client for Lybic's Model Context Protocol (MCP) and its associated RESTful API.

1. List all MCP servers

   method: `list()`
   - args: None
   - return: class dto.ListMcpServerResponse

   ```python
   from lybic import MCP

   mcp = MCP(client)
   mcp_servers = mcp.list()
   for server in mcp_servers:
       print(server)
   ```

   It will out put something like this:

   ```
   id='MCP-xxxx' name='my-mcp-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=False projectId="PRJ-xxxx"
   id='MCP-xxxx' name='default-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=True projectId="PRJ-xxxx"
   ```

2. Create an MCP server

   method: `create(data: dto.CreateMcpServerDto)`
   - args: class dto.CreateMcpServerDto
     - *name: str Name of the MCP server
     - projectId: str (optional) Project to which the server belongs
   - return: class dto.McpServerResponseDto

   ```python
   from lybic import dto, MCP

   mcp = MCP(client)
   new_server = mcp.create(dto.CreateMcpServerDto(name="my-mcp-server"))
   print(new_server)
   ```
   It will out put something like this:
   ```
   id='MCP-xxxx' name='my-mcp-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=False projectId="PRJ-xxxx"
   ```

3. Get the default MCP server

   method: `get_default()`
   - args: None
   - return: class dto.McpServerResponseDto

   ```python
   from lybic import MCP

   mcp = MCP(client)
   default_server = mcp.get_default()
   print(default_server)
   ```
   It will out put something like this:
   ```
   id='MCP-xxxx' name='default-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=True projectId="PRJ-xxxx"
   ```

4. Delete an MCP server

   method: `delete(mcp_server_id: str)`
   - args:
     - *mcp_server_id: str ID of the MCP server to delete
   - return: None(If No http error)

   ```python
   from lybic import MCP

   mcp = MCP(client)
   mcp.delete(mcp_server_id="MCP-xxxx")
   ```

---

The following content has not been **Secondary verification** temporarily


### Class ComputerUse

`ComputerUse` is a client for the Lybic ComputerUse API, used for parsing model outputs and executing actions.

1. Parse model output into computer actions

   method: `parse_model_output(data: dto.ComputerUseParseRequestDto)`
   - args: class dto.ComputerUseParseRequestDto
     - *model: str The model to use (e.g., "ui-tars")
     - *textContent: str The text content to parse
   - return: class dto.ComputerUseActionResponseDto

   ```python
   from lybic import dto, ComputerUse

   computer_use = ComputerUse(client)
   actions = computer_use.parse_model_output(
       dto.ComputerUseParseRequestDto(
           model="ui-tars",
           textContent="click the button"
       )
   )
   print(actions)
   ```

2. Execute a computer use action

   method: `execute_computer_use_action(sandbox_id: str, data: dto.ComputerUseActionDto)`
   - args:
     - *sandbox_id: str ID of the sandbox
     - *data: class dto.ComputerUseActionDto The action to execute
   - return: class dto.SandboxActionResponseDto

   ```python
   from lybic import dto, ComputerUse

   computer_use = ComputerUse(client)
   response = computer_use.execute_computer_use_action(
       sandbox_id="SBX-xxxx",
       data=dto.ComputerUseActionDto(action={"type": "screenshot"})
   )
   print(response)
   ```

### Class Sandbox

`Sandbox` provides methods to manage and interact with sandboxes.

1. List all sandboxes

   method: `list()`
   - args: None
   - return: class dto.SandboxListResponseDto

   ```python
   from lybic import Sandbox

   sandbox = Sandbox(client)
   sandboxes = sandbox.list()
   for s in sandboxes:
       print(s.sandbox)
   ```

2. Create a new sandbox

   method: `create(data: dto.CreateSandboxDto)`
   - args: class dto.CreateSandboxDto
     - name: str (optional) Name for the sandbox
     - maxLifeSeconds: int (optional) Lifetime in seconds
   - return: class dto.GetSandboxResponseDto

   ```python
   from lybic import dto, Sandbox

   sandbox = Sandbox(client)
   new_sandbox = sandbox.create(dto.CreateSandboxDto(name="my-sandbox"))
   print(new_sandbox)
   ```

3. Get a specific sandbox

   method: `get(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: class dto.GetSandboxResponseDto

   ```python
   from lybic import Sandbox

   sandbox = Sandbox(client)
   details = sandbox.get(sandbox_id="SBX-xxxx")
   print(details)
   ```

4. Delete a sandbox

   method: `delete(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox to delete
   - return: None

   ```python
   from lybic import Sandbox

   sandbox = Sandbox(client)
   sandbox.delete(sandbox_id="SBX-xxxx")
   ```

5. Get a sandbox screenshot

   method: `get_screenshot(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: tuple (screenshot_url, PIL.Image.Image, base64_string)

   ```python
   from lybic import Sandbox

   sandbox = Sandbox(client)
   url, image, b64_str = sandbox.get_screenshot(sandbox_id="SBX-xxxx")
   print(f"Screenshot URL: {url}")
   image.show()
   ```