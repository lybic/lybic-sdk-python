## examples

### Asynchronous Usage (Default)

```python
from lybic import LybicClient, LybicAuth

async def main():
    async with LybicClient(
        LybicAuth(
            org_id="ORG-xxxx",
            api_key="lysk-xxxxxxxxxxx",
            endpoint="https://api.lybic.cn/",
        )
    ) as client:
        pass
```

### Synchronous Usage

The Lybic SDK also provides synchronous clients with the same API interface. Simply import from `lybic_sync` instead of `lybic`:

```python
from lybic_sync import LybicSyncClient, LybicAuth

# No async/await needed!
with LybicSyncClient(
    LybicAuth(
        org_id="ORG-xxxx",
        api_key="lysk-xxxxxxxxxxx",
        endpoint="https://api.lybic.cn/",
    )
) as client:
    # Use the client directly without await
    sandboxes = client.sandbox.list()
    stats = client.stats.get()
```

**Note:** All examples below show the async version. For synchronous usage, replace:
- `from lybic import LybicClient` → `from lybic_sync import LybicSyncClient`
- `async with LybicClient()` → `with LybicSyncClient()`
- `await client.method()` → `client.method()` (remove `await`)
- Remove `async def` and `asyncio.run()` wrappers

### LybicClient Manual lifecycle management

From v0.5.4, we've added a new feature that allows developers to manually manage the LybicClient lifecycle for increased 
flexibility.

However, please note that this introduces certain risks, and we still recommend using the `async with ... as ...` syntax.

**Async version:**

```python
import asyncio 
from lybic import LybicClient, LybicAuth

client = LybicClient(LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx"))

async def main():
    await client.request("GET", f"/api/orgs/{client.org_id}/stats")
    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
```

**Sync version:**

```python
from lybic_sync import LybicSyncClient, LybicAuth

client = LybicSyncClient(LybicAuth(org_id="ORG-xxxx", api_key="lysk-xxxxxxxxxxx"))

# No asyncio needed!
response = client.request("GET", f"/api/orgs/{client.org_id}/stats")
client.close()
```

### Class Stats

`Stats` is a class for describing the stats of the organization.

1. Get the stats of the organization

    such as number of members, computers, etc.

    method: `get()`
    - args: None
    - return: class dto.StatsResponseDto

    **Async version:**
    ```python
    from lybic import Stats
    # Inside your async main function, with the client initialized:
    stats = Stats(client)
    print(await stats.get())
    ```
    
    **Sync version:**
    ```python
    from lybic_sync import StatsSync
    # With the sync client initialized:
    stats = StatsSync(client)
    print(stats.get())  # No await!
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
   import asyncio
   from lybic import Project
   # Inside your async main function, with the client initialized:
   project = Project(client)
   list_result = await project.list()
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
   
   method: `create(data: dto.CreateMcpServerDto)` or `create(**kwargs)`
   - args: class dto.CreateProjectDto
     - *name: str project name
   - return: class dto.SingleProjectResponseDto

   ```python
   import asyncio
   from lybic import dto
   from lybic import Project
   
   # Inside your async main function, with the client initialized:
   project = Project(client)
   # Using DTO
   print(await project.create(dto.CreateProjectDto(name="test_project")))
   # Using keyword arguments
   print(await project.create(name="test_project_2"))
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
   import asyncio
   from lybic import Project
   # Inside your async main function, with the client initialized:
   project = Project(client)
   await project.delete(project_id="PRJ-xxxx")
   ```

### Class MCP

`MCP` is a client for Lybic's Model Context Protocol (MCP) and its associated RESTful API.

1. List all MCP servers

   method: `list()`
   - args: None
   - return: class dto.ListMcpServerResponse

   ```python
   import asyncio
   from lybic import MCP

   mcp = MCP(client)
   mcp_servers = asyncio.run(mcp.list())
   for server in mcp_servers:
       print(server)
   ```

   It will out put something like this:

   ```
   id='MCP-xxxx' name='my-mcp-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=False projectId="PRJ-xxxx"
   id='MCP-xxxx' name='default-server' createdAt='2025-07-08T16:42:30.226Z' defaultMcpServer=True projectId="PRJ-xxxx"
   ```

2. Create an MCP server

   method: `create(data: dto.CreateMcpServerDto)` or `create(**kwargs)`
   - args: class dto.CreateMcpServerDto
     - *name: str Name of the MCP server
     - projectId: str (optional) Project to which the server belongs
   - return: class dto.McpServerResponseDto

   ```python
   from lybic import dto, MCP

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   # Using DTO
   new_server = await mcp.create(dto.CreateMcpServerDto(name="my-mcp-server"))
   print(new_server)
   # Using keyword arguments
   new_server_2 = await mcp.create(name="my-mcp-server-2")
   print(new_server_2)
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
   import asyncio
   from lybic import MCP
   
   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   default_server = await mcp.get_default()
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

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   await mcp.delete(mcp_server_id="MCP-xxxx")
   ```

5. Set MCP server to a sandbox

   method: `set_sandbox(mcp_server_id: str, sandbox_id: str)`
   - args:
     - *mcp_server_id: str ID of the MCP server
     - *sandbox_id: str ID of the sandbox to connect the MCP server to
   - return: None(If No http error)

   ```python
   from lybic import MCP

   # Inside your async main function, with the client initialized:
   mcp = MCP(client)
   await mcp.set_sandbox(mcp_server_id="MCP-xxxx", sandbox_id="SBX-xxxx")
   ```

### Class ComputerUse

`ComputerUse` is a client for the Lybic ComputerUse API, used for parsing model outputs and executing actions.

1. Parse LLM output into computer action

   If you want to parse the model output, you can use this method.

   method: `parse_llm_output(model_type: dto.ModelType | str, llm_output: str)`
   - args: 
     - *model_type: The type of the large language model.
     - *llm_output: The text output from the large language model.
   - return: class dto.ComputerUseActionResponseDto

   If the model you use is "ui-tars", and its prompts like this:

   ```markdown
   You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.

   ## Output Format
    \```
    Thought: ...
    Action: ...
    \```
   
   ## Action Space
   click(point='<point>x1 y1</point>')
   left_double(point='<point>x1 y1</point>')
   right_single(point='<point>x1 y1</point>')
   drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
   hotkey(key='ctrl c') # Split keys with a space and use lowercase. Also, do not use more than 3 keys in one hotkey action.
   type(content='xxx') # Use escape characters \', \", and \n in content part to ensure we can parse the content in normal python string format. If you want to submit your input, use \n at the end of content. 
   scroll(point='<point>x1 y1</point>', direction='down or up or right or left') # Show more information on the `direction` side.
   wait() #Sleep for 5s and take a screenshot to check for any changes.
   finished(content='xxx') # Use escape characters \', \", and \n in content part to ensure we can parse the content in normal python string format.
   
   ## Note
   - Use {language} in `Thought` part.
   - Write a small plan and finally summarize your next action (with its target element) in one sentence in `Thought` part.
   
   ## User Instruction
   {instruction}
   ```

   The model output like this:

   ```
   Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.

   Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
   Action: left_double(point='<point>213 257</point>')
   ```

   This api will parse this model output format and return a list of computer use actions.

   ```python
   import asyncio
   from lybic import LybicClient, dto, ComputerUse, LybicAuth

   async def main():
       async with LybicClient(
            LybicAuth(
               org_id="ORG-xxxx",
               api_key="lysk-xxxxxxxxxxx",
               endpoint="https://api.lybic.cn/",
            )
       ) as client:
           computer_use = ComputerUse(client)
           text_content = """Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.
        
           Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
           Action: left_double(point='<point>213 257</point>')"""
           
           actions = await computer_use.parse_llm_output(
               model_type="ui-tars",
               llm_output=text_content
           )
           print(actions)

   if __name__ == "__main__":
       asyncio.run(main())
   ```
   It will out put something like this:(an action list object,and length is 1)

   ```
   actions=[MouseDoubleClickAction(type='mouse:doubleClick', x=FractionalLength(type='/', numerator=213, denominator=1000), y=FractionalLength(type='/', numerator=257, denominator=1000), button=1)]
   ```

### Class Sandbox

`Sandbox` provides methods to manage and interact with sandboxes.

1. List all sandboxes

   method: `list()`
   - args: None
   - return: class dto.SandboxListResponseDto

   ```python
   from lybic import LybicClient
   # Inside your async main function, with the client initialized:
   async def list():
     client = LybicClient()  # Initialize your client here
     sandboxes = await client.sandbox.list()
     for s in sandboxes:
         print(s)
   ```
   It will out put something like this:
   ```
   id='SBX-xxxxx' name='xxxx' expiredAt='2025-07-25T07:21:31.026Z' expiresAt='2025-07-25T07:21:31.026Z' createdAt='2025-07-25T06:21:31.027Z' projectId='PRJ-xxxxxxx'
   id='SBX-xxxxx' name='xxxx' expiredAt='2025-07-26T08:24:11.198Z' expiresAt='2025-07-26T08:24:11.198Z' createdAt='2025-07-26T07:24:11.199Z' projectId='PRJ-xxxxxxx'
   ```

2. Create a new sandbox

   method: `create(data: dto.CreateSandboxDto)` or `create(**kwargs)`
   - args: class dto.CreateSandboxDto
     - name: str (optional) Name for the sandbox, if not provided, it will use a default name(sandbox).
     - maxLifeSeconds: int (optional) Lifetime in seconds, if not provided, it will use the default value of 3600 seconds (1 hour).
     - projectId: str (optional) Project ID to associate with the sandbox,if not provided, it will use the default project.
     - shape: str The shape of the sandbox.
   - return: class dto.GetSandboxResponseDto

   ```python
   from lybic import dto, LybicClient
   async def main():
      # Inside your async main function, with the client initialized:
      client = LybicClient()
      # Using DTO
      new_sandbox = await client.sandbox.create(dto.CreateSandboxDto(name="my-sandbox", shape="xxx"))
      print(new_sandbox)
      # Using keyword arguments
      new_sandbox_2 = await client.sandbox.create(name="my-sandbox-2", shape="xxx")
      print(new_sandbox_2)
   ```

3. Get a specific sandbox

   method: `get(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: class dto.GetSandboxResponseDto

   ```python
   from lybic import dto, LybicClient
   async def main():
       async with LybicClient(
           dto.LybicAuth(
               org_id="ORG-xxxx",
               api_key="lysk-xxxxxxxxxxx",
               endpoint="https://api.lybic.cn/",
           )
       ) as client:
           details = await client.sandbox.get(sandbox_id="SBX-xxxx")
           print(details)
   ```

4. Delete a sandbox

   method: `delete(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox to delete
   - return: None

   ```python
   import asyncio
   from lybic import LybicClient,LybicAuth
   async def main():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/",
            )
        ) as client:
            await client.sandbox.delete(sandbox_id="SBX-xxxx")
   ```

5. Get a sandbox screenshot

   method: `get_screenshot(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: tuple (screenshot_url, PIL.Image.Image, webp_image_base64_string)

   ```python
   import asyncio
   from lybic import LybicClient,LybicAuth
   async def main():
         async with LybicClient(
             LybicAuth(
                 org_id="ORG-xxxx",
                 api_key="lysk-xxxxxxxxxxx",
                 endpoint="https://api.lybic.cn/",
             )
         ) as client:
             screenshot_url, image, webp_base64 = await client.sandbox.get_screenshot(sandbox_id="SBX-xxxx")
             print("Screenshot URL:", screenshot_url)
             image.show()  # Display the image using PIL
             print("WebP Base64 String:", webp_base64)
   ```

6. Extend a sandbox's lifetime

    method: `extend_life(sandbox_id: str, seconds: int)`
    - args:
      - *sandbox_id: str ID of the sandbox
      - *seconds: int Lifetime in seconds to extend the sandbox's lifetime (default: 3600 s, 1 hour, max: 86400 s, 1 day)
    - return: None(if successful)

    ```python
    import asyncio
    from lybic import LybicClient,LybicAuth
    async def main():
         async with LybicClient(
             LybicAuth(
                 org_id="ORG-xxxx",
                 api_key="lysk-xxxxxxxxxxx",
                 endpoint="https://api.lybic.cn/",
             )
         ) as client:
             await client.sandbox.extend_life(sandbox_id="SBX-xxxx", seconds=7200)  # Extend by 2 hours
    ```

7. Execute a sandbox action

   This interface enables `Planner` to perform actions on the sandbox through Restful calls. It supports both computer use and mobile use actions.
   
   method: `execute_sandbox_action(sandbox_id: str, data: dto.ExecuteSandboxActionDto)` or `execute_sandbox_action(sandbox_id: str, **kwargs)`
   - args:
     - *sandbox_id: str ID of the sandbox
     - *data: class dto.ExecuteSandboxActionDto The action to execute
   - return: class dto.SandboxActionResponseDto

   ```python
   import asyncio
   from lybic import dto, Sandbox, LybicClient, LybicAuth
   async def main():
       async with LybicClient(
         LybicAuth(
            org_id="ORG-xxxx",
            api_key="lysk-xxxxxxxxxxx",
            endpoint="https://api.lybic.cn/",
       )
     ) as client:
           parsed_result = await client.computer_use.parse_llm_output(
               model_type="ui-tars",
               llm_output="""Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.
     
           Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
           Action: left_double(point='<point>213 257</point>')"""
           )
           actions = parsed_result.actions
           if actions:
               # Using DTO
               response = await client.sandbox.execute_sandbox_action(
                   sandbox_id="SBX-xxxx",
                   data=dto.ExecuteSandboxActionDto(action=actions[0])
               )
               print(response)
               # Using keyword arguments
               response_2 = await client.sandbox.execute_sandbox_action(
                   sandbox_id="SBX-xxxx",
                   action=actions[0]
               )
               print(response_2)
   if __name__ == "__main__":
       asyncio.run(main())
   ```

8. Copy files between sandbox and external storage (Unified file transfer method)

   The `copy_files` method provides a unified way to transfer files bidirectionally between the sandbox and external locations (HTTP/S3). It supports multiple file location types and batch operations.

   method: `copy_files(sandbox_id: str, data: dto.SandboxFileCopyRequestDto)` or `copy_files(sandbox_id: str, **kwargs)`
   - args:
     - data: dto.SandboxFileCopyRequestDto
       - files: List[dto.FileCopyItem]
         - index: int (unique identifier for tracking each file operation)
         - src: FileLocation (source location)
         - dest: FileLocation (destination location)
   - return: dto.SandboxFileCopyResponseDto
     - results: List[dto.FileCopyResult]
       - index: int
       - success: bool
       - error: Optional[str]

   **Supported File Location Types:**
   - `SandboxFileLocation`: File path within the sandbox
   - `HttpPutLocation`: HTTP PUT upload URL (for uploading files)
   - `HttpGetLocation`: HTTP GET download URL (for downloading files)
   - `HttpPostFormLocation`: HTTP POST multipart form upload (for services requiring form uploads)

   **8.1 Upload files from local machine to sandbox (MinIO end-to-end example)**

   **Workflow:**
   The overall process is: upload file to object storage → generate presigned GET URL → sandbox downloads from URL.
   
   ```mermaid
   sequenceDiagram
       participant User
       participant MinIO as Object Storage
       participant Sandbox

       User->>MinIO: Upload local file
       MinIO-->>User: Generate presigned GET URL
       User->>Sandbox: Call copy_files() with HttpGetLocation
       Sandbox->>MinIO: Download file from URL
       MinIO-->>Sandbox: File content
       Sandbox->>Sandbox: Save to destination path
   ```

   **Prerequisites:**
   - Install minio SDK: `pip install minio`
   - You have a MinIO instance and bucket (e.g. `agent-data`)

   **Complete workflow:**
   1. Upload local file to MinIO using MinIO SDK
   2. Generate a presigned GET URL for the uploaded object
   3. Call Lybic `sandbox.copy_files()` with HttpGetLocation (source) and SandboxFileLocation (destination)
   4. Sandbox downloads the file from the URL and saves it to the specified path

   ```python
   import asyncio
   from datetime import timedelta
   from minio import Minio
   from lybic import LybicClient, LybicAuth
   from lybic.dto import (
       SandboxFileCopyRequestDto, 
       FileCopyItem, 
       SandboxFileLocation, 
       HttpGetLocation
   )

   # MinIO configuration
   MINIO_ENDPOINT = 'play.min.io'  # Replace with your MinIO endpoint
   ACCESS_KEY = 'Q3AM3UQ867SPQQA43P2F'
   SECRET_KEY = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
   USE_SECURE = True
   BUCKET = 'agent-data'

   # File configuration
   LOCAL_FILE_PATH = './local_input.txt'  # Local file to upload
   OBJECT_NAME = 'uploads/input.txt'  # Object key in MinIO
   SANDBOX_PATH = '/home/agent/input.txt'  # Destination path in sandbox

   async def upload_file_to_sandbox():
       # Step 1: Upload local file to MinIO
       minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=USE_SECURE)
       
       # Ensure bucket exists
       if not minio_client.bucket_exists(BUCKET):
           minio_client.make_bucket(BUCKET)
           print(f"Created bucket: {BUCKET}")
       
       # Upload file to MinIO
       minio_client.fput_object(BUCKET, OBJECT_NAME, LOCAL_FILE_PATH)
       print(f"Uploaded {LOCAL_FILE_PATH} to MinIO as {OBJECT_NAME}")
       
       # Step 2: Generate presigned GET URL (valid for 1 hour)
       presigned_url = minio_client.presigned_get_object(
           BUCKET, OBJECT_NAME, expires=timedelta(minutes=60)
       )
       print(f"Generated presigned URL: {presigned_url}")
       
       # Step 3: Use Lybic SDK to copy file from URL to sandbox
       async with LybicClient(
           LybicAuth(
               org_id='ORG-xxxx',
               api_key='lysk-xxxxxxxxxxx',
               endpoint='https://api.lybic.cn/'
           )
       ) as client:
           response = await client.sandbox.copy_files(
               'SBX-xxxx',  # Your sandbox ID
               SandboxFileCopyRequestDto(files=[
                   FileCopyItem(
                       src=HttpGetLocation(url=presigned_url),
                       dest=SandboxFileLocation(path=SANDBOX_PATH)
                   )
               ])
           )
           
           print("Copy result:", response)
           for result in response.results:
               if result.success:
                   print(f"✓ File successfully copied to sandbox (index: {result.id})")
               else:
                   print(f"✗ Failed to copy file (index: {result.id}): {result.error}")

   if __name__ == '__main__':
       asyncio.run(upload_file_to_sandbox())
   ```

   **8.2 Download files from sandbox to local machine (MinIO end-to-end example)**

   **Workflow:**
   ```mermaid
   sequenceDiagram
       participant User
       participant MinIO as Object Storage
       participant Sandbox

       User->>MinIO: Request presigned PUT URL
       MinIO-->>User: Generate presigned PUT URL
       User->>Sandbox: Call copy_files() with HttpPutLocation
       Sandbox->>MinIO: Upload file to presigned URL
       MinIO-->>Sandbox: Upload success
       User->>MinIO: Download file
       MinIO-->>User: File content
   ```

   **Complete workflow:**
   1. Generate a presigned PUT URL using MinIO SDK
   2. Call Lybic `sandbox.copy_files()` with SandboxFileLocation (source) and HttpPutLocation (destination)
   3. Sandbox uploads its local file to the presigned URL
   4. Download the file from MinIO to your local machine

   ```python
   import asyncio
   from datetime import timedelta
   from minio import Minio
   from lybic import LybicClient, LybicAuth
   from lybic.dto import (
       SandboxFileCopyRequestDto, 
       FileCopyItem, 
       SandboxFileLocation, 
       HttpPutLocation
   )

   # MinIO configuration
   MINIO_ENDPOINT = 'play.min.io'
   ACCESS_KEY = 'Q3AM3UQ867SPQQA43P2F'
   SECRET_KEY = 'zuf+tfteSlswRu7BJ86wekitnifILbZam1KYY3TG'
   USE_SECURE = True
   BUCKET = 'agent-data'

   # File configuration
   SANDBOX_FILE_PATH = '/home/agent/data/output.txt'  # File path in sandbox
   OBJECT_NAME = 'downloads/output.txt'  # Target object key in MinIO
   LOCAL_DOWNLOAD_PATH = './downloaded_output.txt'  # Local destination

   async def download_file_from_sandbox():
       minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=USE_SECURE)
       
       # Ensure bucket exists
       if not minio_client.bucket_exists(BUCKET):
           minio_client.make_bucket(BUCKET)
           print(f"Created bucket: {BUCKET}")
       
       # Step 1: Generate presigned PUT URL (valid for 1 hour)
       presigned_put_url = minio_client.presigned_put_object(
           BUCKET, OBJECT_NAME, expires=timedelta(minutes=60)
       )
       print(f"Generated presigned PUT URL: {presigned_put_url}")
       
       # Step 2: Use Lybic SDK to copy file from sandbox to URL
       async with LybicClient(
           LybicAuth(
               org_id='ORG-xxxx',
               api_key='lysk-xxxxxxxxxxx',
               endpoint='https://api.lybic.cn/'
           )
       ) as client:
           response = await client.sandbox.copy_files(
               'SBX-xxxx',  # Your sandbox ID
               SandboxFileCopyRequestDto(files=[
                   FileCopyItem(
                       src=SandboxFileLocation(path=SANDBOX_FILE_PATH),
                       dest=HttpPutLocation(url=presigned_put_url)
                   )
               ])
           )
           
           print("Copy result:", response)
           for result in response.results:
               if result.success:
                   print(f"✓ File successfully copied from sandbox (index: {result.id})")
               else:
                   print(f"✗ Failed to copy file (index: {result.id}): {result.error}")
       
       # Step 3: Download the file from MinIO to local machine
       minio_client.fget_object(BUCKET, OBJECT_NAME, LOCAL_DOWNLOAD_PATH)
       print(f"Downloaded file from MinIO to {LOCAL_DOWNLOAD_PATH}")
       
       # Step 4: Verify the file
       with open(LOCAL_DOWNLOAD_PATH, 'r') as f:
           content = f.read()
           print(f"File content preview: {content[:100]}...")

   if __name__ == '__main__':
       asyncio.run(download_file_from_sandbox())
   ```

   **8.3 Batch copy multiple files**

   Copy multiple files in a single request (mixed directions):

   ```python
   from lybic.dto import (
       SandboxFileCopyRequestDto, 
       FileCopyItem, 
       SandboxFileLocation, 
       HttpGetLocation,
       HttpPutLocation
   )

   # Copy multiple files: some from external to sandbox, some from sandbox to external
   response = await client.sandbox.copy_files(
       'SBX-xxxx',
       SandboxFileCopyRequestDto(files=[
           # Download from URL to sandbox
           FileCopyItem(
               src=HttpGetLocation(url='https://example.com/file1.txt'),
               dest=SandboxFileLocation(path='/home/agent/file1.txt')
           ),
           # Upload from sandbox to URL
           FileCopyItem(
               src=SandboxFileLocation(path='/home/agent/output.log'),
               dest=HttpPutLocation(url='https://s3.example.com/output.log')
           ),
           # Another download
           FileCopyItem(
               src=HttpGetLocation(url='https://example.com/file2.txt'),
               dest=SandboxFileLocation(path='/home/agent/file2.txt')
           )
       ])
   )

   # Check results by index
   for result in response.results:
       if result.success:
           print(f"✓ File {result.id} copied successfully")
       else:
           print(f"✗ File {result.id} failed: {result.error}")
   ```

   **8.4 Using HTTP POST multipart form upload**

   For services that require multipart form uploads (e.g., some AWS S3 presigned POST policies):

   ```python
   from minio import Minio, PostPolicy
   from datetime import datetime, timedelta
   from lybic.dto import (
       SandboxFileCopyRequestDto, 
       FileCopyItem, 
       SandboxFileLocation, 
       HttpPostFormLocation
   )

   # Generate POST policy with MinIO
   minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=USE_SECURE)
   
   policy = PostPolicy()
   policy.set_bucket(BUCKET)
   policy.set_key('uploads/report.pdf')
   policy.set_expires(datetime.now(datetime.UTC) + timedelta(hours=1))
   
   form_data = minio_client.presigned_post_policy(policy)
   
   # Use POST form for upload
   response = await sandbox.copy_files(
       'SBX-xxxx',
       SandboxFileCopyRequestDto(files=[
           FileCopyItem(
               src=SandboxFileLocation(path='/home/agent/report.pdf'),
               dest=HttpPostFormLocation(
                   url=form_data['url'],
                   form={k: v for k, v in form_data.items() if k != 'url'},
                   fileField='file'  # Form field name for the file
               )
           )
       ])
   )
   ```

   **8.5 With custom headers**

   Add custom headers for authentication or other purposes:

   ```python
   from lybic.dto import HttpPutLocation, HttpGetLocation

   # GET with custom headers (e.g., authentication)
   response = await sandbox.copy_files(
       'SBX-xxxx',
       SandboxFileCopyRequestDto(files=[
           FileCopyItem(
               src=HttpGetLocation(
                   url='https://api.example.com/files/data.json',
                   headers={
                       'Authorization': 'Bearer YOUR_TOKEN',
                       'X-Custom-Header': 'value'
                   }
               ),
               dest=SandboxFileLocation(path='/home/agent/data.json')
           )
       ])
   )

   # PUT with custom headers
   response = await sandbox.copy_files(
       'SBX-xxxx',
       SandboxFileCopyRequestDto(files=[
           FileCopyItem(
               src=SandboxFileLocation(path='/home/agent/result.json'),
               dest=HttpPutLocation(
                   url='https://storage.example.com/uploads/result.json',
                   headers={
                       'Content-Type': 'application/json',
                       'X-Upload-Id': 'unique-id'
                   }
               )
           )
       ])
   )
   ```

9. Legacy file transfer methods (Deprecated)

   > [!WARNING]
   > The `upload_files` and `download_files` methods have been removed in favor of the unified `copy_files` method.
   > Please migrate your code to use `copy_files` as shown in section 8 above.

10. Execute a process inside a sandbox

    Run an executable with arguments; capture stdout/stderr (base64-encoded) and exit code.
    
    method: `execute_process(sandbox_id: str, data: dto.SandboxProcessRequestDto)` or `execute_process(sandbox_id: str, executable=..., ...)`
    - args:
      - executable: str (absolute or resolvable path in sandbox, e.g. `/usr/bin/python3`)
      - args: List[str]
      - workingDirectory: Optional[str]
      - stdinBase64: Optional[str] (base64-encoded bytes to feed to stdin)
    - return: dto.SandboxProcessResponseDto { stdoutBase64, stderrBase64, exitCode }

    ```python
    import asyncio
    import base64
    from lybic import dto, LybicClient, LybicAuth

    async def run_process_example():
        async with LybicClient(LybicAuth(org_id='ORG-xxxx', api_key='lysk-xxxxxxxxxxx')) as client:
            # Example 1: Simple command
            result = await client.sandbox.execute_process(
                'SBX-xxxx',
                executable='/bin/echo',
                args=['Hello', 'World']
            )
            print(f"Exit code: {result.exitCode}")
            stdout = base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')
            print(f"Output: {stdout}")
            
            # Example 2: Python script with stdin
            stdin_data = base64.b64encode(b"print('Hello from stdin')\n").decode()
            proc_req = dto.SandboxProcessRequestDto(
                executable='/usr/bin/python3',
                args=['-c', 'import sys; exec(sys.stdin.read())'],
                workingDirectory='/home/agent',
                stdinBase64=stdin_data
            )
            result = await client.sandbox.execute_process('SBX-xxxx', data=proc_req)
            print(f"Exit: {result.exitCode}")
            print(f"STDOUT: {base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')}")
            print(f"STDERR: {base64.b64decode(result.stderrBase64 or '').decode(errors='ignore')}")

    if __name__ == '__main__':
        asyncio.run(run_process_example())
    ```

11. Create a sandbox from a machine image

    Create a new sandbox using a previously saved machine image. This allows you to start sandboxes with pre-configured environments and installed software.

    method: `create_from_image(data: dto.CreateSandboxFromImageDto)` or `create_from_image(**kwargs)`
    - args:
      - imageId: str (required) The machine image ID to create sandbox from
      - name: str (optional) The name of the sandbox (default: "sandbox")
      - maxLifeSeconds: int (optional) Maximum lifetime in seconds (default: 3600, min: 300, max: 604800)
      - projectId: str (optional) Project ID to associate with the sandbox
    - return: dto.CreateSandboxFromImageResponseDto

    ```python
    import asyncio
    from lybic import dto, LybicClient, LybicAuth

    async def create_from_image_example():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/"
            )
        ) as client:
            # Using DTO
            sandbox = await client.sandbox.create_from_image(
                dto.CreateSandboxFromImageDto(
                    imageId="IMG-xxxx",
                    name="my-sandbox-from-image",
                    maxLifeSeconds=7200
                )
            )
            print(f"Created sandbox: {sandbox}")
            
            # Using keyword arguments
            sandbox2 = await client.sandbox.create_from_image(
                imageId="IMG-xxxx",
                name="my-sandbox-2",
                maxLifeSeconds=3600,
                projectId="PRJ-xxxx"
            )
            print(f"Created sandbox 2: {sandbox2}")

    if __name__ == '__main__':
        asyncio.run(create_from_image_example())
    ```

12. Get sandbox status

    Get the current status of a sandbox (PENDING/RUNNING/STOPPED/ERROR).

    method: `get_status(sandbox_id: str)`
    - args:
      - sandbox_id: str ID of the sandbox
    - return: dto.SandboxStatus (Enum: PENDING, RUNNING, STOPPED, ERROR)

    ```python
    import asyncio
    from lybic import LybicClient, LybicAuth

    async def get_status_example():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/"
            )
        ) as client:
            status = await client.sandbox.get_status("SBX-xxxx")
            print(f"Sandbox status: {status}")
            
            # Check status conditionally
            if status == "RUNNING":
                print("Sandbox is ready to use")
            elif status == "PENDING":
                print("Sandbox is starting up...")
            elif status == "ERROR":
                print("Sandbox encountered an error")
            elif status == "STOPPED":
                print("Sandbox has been stopped")

    if __name__ == '__main__':
        asyncio.run(get_status_example())
    ```

13. Create a machine image from a sandbox

    Create a machine image (snapshot) from an existing sandbox. This captures the current state of the sandbox including installed software, files, and configurations.

    method: `create_machine_image(data: dto.CreateMachineImageDto)` or `create_machine_image(**kwargs)`
    - args:
      - sandboxId: str (required) The sandbox ID to create image from
      - name: str (required) The name of the machine image (1-100 characters)
      - description: str (optional) Optional description (max 500 characters)
    - return: dto.MachineImageResponseDto

    ```python
    import asyncio
    from lybic import dto, LybicClient, LybicAuth

    async def create_image_example():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/"
            )
        ) as client:
            # Using DTO
            image = await client.sandbox.create_machine_image(
                dto.CreateMachineImageDto(
                    sandboxId="SBX-xxxx",
                    name="my-configured-environment",
                    description="Ubuntu with Python 3.11 and dependencies installed"
                )
            )
            print(f"Created image: {image.id}")
            print(f"Image name: {image.name}")
            print(f"Created at: {image.createdAt}")
            
            # Using keyword arguments
            image2 = await client.sandbox.create_machine_image(
                sandboxId="SBX-yyyy",
                name="dev-environment",
                description="Development environment with tools"
            )
            print(f"Created image 2: {image2.id}")

    if __name__ == '__main__':
        asyncio.run(create_image_example())
    ```

14. List machine images

    List all machine images in your organization.

    method: `list_machine_images()`
    - args: None
    - return: dto.MachineImagesResponseDto (contains list of images and quota information)

    ```python
    import asyncio
    from lybic import LybicClient, LybicAuth

    async def list_images_example():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/"
            )
        ) as client:
            result = await client.sandbox.list_machine_images()
            
            print(f"Total images: {len(result.images)}")
            print(f"Quota: {result.quota.used}/{result.quota.limit}")
            
            for image in result.images:
                print(f"ID: {image.id}")
                print(f"  Name: {image.name}")
                print(f"  Description: {image.description}")
                print(f"  Shape: {image.shapeName}")
                print(f"  Created: {image.createdAt}")
                print(f"  Size: {image.size} bytes")
                print()

    if __name__ == '__main__':
        asyncio.run(list_images_example())
    ```

15. Delete a machine image

    Delete a machine image from your organization.

    method: `delete_machine_image(image_id: str)`
    - args:
      - image_id: str ID of the machine image to delete
    - return: None

    ```python
    import asyncio
    from lybic import LybicClient, LybicAuth

    async def delete_image_example():
        async with LybicClient(
            LybicAuth(
                org_id="ORG-xxxx",
                api_key="lysk-xxxxxxxxxxx",
                endpoint="https://api.lybic.cn/"
            )
        ) as client:
            await client.sandbox.delete_machine_image("IMG-xxxx")
            print("Machine image deleted successfully")

    if __name__ == '__main__':
        asyncio.run(delete_image_example())
    ```

### Error Handling

The SDK provides user-friendly exceptions for API errors instead of raw HTTP errors.

#### Exception Classes

- `LybicError`: Base exception class for all Lybic SDK errors
- `LybicAPIError`: For API errors with structured responses (containing 'code' and 'message' fields)
- `LybicInternalError`: For 5xx reverse proxy errors that return HTML pages

#### Basic Error Handling

```python
from lybic import LybicClient, LybicAPIError, LybicInternalError

async with LybicClient() as client:
    try:
        # Example API call that might fail
        result = await client.request("GET", "/api/orgs/test/sandboxes/invalid-id")
    except LybicAPIError as e:
        # Handle structured API errors (4xx/5xx with JSON response)
        print(f"❌ API Error: {e.message}")
        if e.code:
            print(f"   Error Code: {e.code}")
        print(f"   HTTP Status: {e.status_code}")
    except LybicInternalError as e:
        # Handle reverse proxy 5xx errors (HTML response)
        print(f"❌ {e.message}")
        print(f"   HTTP Status: {e.status_code}")
    except Exception as e:
        # Handle other errors (network issues, timeouts, etc.)
        print(f"❌ Unexpected error: {e}")
```

#### Structured API Errors

When the API returns a structured error like:
```json
{"code": "nomos.partner.NO_ROOMS_AVAILABLE", "message": "No rooms available"}
```

The SDK will raise `LybicAPIError` with:
- `message`: "No rooms available"
- `code`: "nomos.partner.NO_ROOMS_AVAILABLE"
- `status_code`: HTTP status code (e.g., 400, 404, 500)

Example:
```python
from lybic import LybicClient, LybicAPIError

async with LybicClient() as client:
    try:
        result = await client.request("POST", "/api/some-endpoint")
    except LybicAPIError as e:
        # You can access individual error properties
        print(f"Error message: {e.message}")
        print(f"Error code: {e.code}")
        print(f"Status code: {e.status_code}")
        
        # The string representation includes both message and code
        print(f"Full error: {e}")
        # Output: "No rooms available (code: nomos.partner.NO_ROOMS_AVAILABLE)"
```

#### Internal Server Errors

When a 5xx error occurs at the reverse proxy level and returns HTML instead of JSON, the SDK will raise `LybicInternalError` with:
- `message`: "internal error occur"
- `status_code`: HTTP status code (e.g., 500, 502, 503)

Example:
```python
from lybic import LybicClient, LybicInternalError

async with LybicClient() as client:
    try:
        result = await client.request("GET", "/api/endpoint")
    except LybicInternalError as e:
        print(f"Internal error: {e.message}")  # "internal error occur"
        print(f"Status code: {e.status_code}")
```

#### Catching All Lybic Errors

You can catch `LybicError` to handle all SDK-specific errors, or catch specific exceptions for more granular handling:

```python
from lybic import LybicClient, LybicError

async with LybicClient() as client:
    try:
        result = await client.request("GET", "/api/endpoint")
    except LybicError as e:
        # This catches both LybicAPIError and LybicInternalError
        print(f"Lybic SDK error: {e.message}")
        print(f"Status code: {e.status_code}")
```
