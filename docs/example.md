## examples

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

### LybicClient Manual lifecycle management

From v0.5.4, we've added a new feature that allows developers to manually manage the LybicClient lifecycle for increased 
flexibility.

However, please note that this introduces certain risks, and we still recommend using the `async with ... as ...` syntax.

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

### Class Stats

`Stats` is a class for describing the stats of the organization.

1. Get the stats of the organization

    such as number of members, computers, etc.

    method: `get()`
    - args: None
    - return: class dto.StatsResponseDto

    ```python
    from lybic import Stats
    # Inside your async main function, with the client initialized:
    stats = Stats(client)
    print(await stats.get())
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
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   sandboxes = await sandbox.list()
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
   from lybic import dto, Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   # Using DTO
   new_sandbox = await sandbox.create(dto.CreateSandboxDto(name="my-sandbox", shape="xxx"))
   print(new_sandbox)
   # Using keyword arguments
   new_sandbox_2 = await sandbox.create(name="my-sandbox-2", shape="xxx")
   print(new_sandbox_2)
   ```

3. Get a specific sandbox

   method: `get(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: class dto.GetSandboxResponseDto

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   details = await sandbox.get(sandbox_id="SBX-xxxx")
   print(details)
   ```

   It will out put something like this:

   ```
   sandbox=Sandbox(id='SBX-xxxx', name='xxxx', expiredAt='2025-07-26T08:24:11.198Z', expiresAt='2025-07-26T08:24:11.198Z', createdAt='2025-07-26T07:24:11.199Z', projectId='PRJ-xxxx'), connectDetails=ConnectDetails(gatewayAddresses=[GatewayAddress(address='1.2.3.4', port=12345, name='0197e397-5394-7880-a314-d8a7e981f9e4', preferredProviders=[1], gatewayType=4)], certificateHashBase64='baes64str==', endUserToken='jwttokenbase64str')
   ```

4. Delete a sandbox

   method: `delete(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox to delete
   - return: None

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   await sandbox.delete(sandbox_id="SBX-xxxx")
   ```

5. Get a sandbox screenshot

   method: `get_screenshot(sandbox_id: str)`
   - args:
     - *sandbox_id: str ID of the sandbox
   - return: tuple (screenshot_url, PIL.Image.Image, webp_image_base64_string)

   ```python
   import asyncio
   from lybic import Sandbox

   # Inside your async main function, with the client initialized:
   sandbox = Sandbox(client)
   url, image, b64_str = await sandbox.get_screenshot(sandbox_id="SBX-xxxx")
   print(f"Screenshot URL: {url}")
   image.show()
   ```

6. Extend a sandbox's lifetime

    method: `extend_life(sandbox_id: str, seconds: int)`
    - args:
      - *sandbox_id: str ID of the sandbox
      - *seconds: int Lifetime in seconds to extend the sandbox's lifetime (default: 3600 s, 1 hour, max: 86400 s, 1 day)
    - return: None(if successful)

    ```python
    import asyncio
    from lybic import Sandbox
   
    # Inside your async main function, with the client initialized:
    sandbox = Sandbox(client)
    await sandbox.extend_life(sandbox_id="SBX-xxxx", seconds=3600)
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
   from lybic import dto, Sandbox, ComputerUse, LybicClient, LybicAuth
   async def main():
       async with LybicClient(
         LybicAuth(
            org_id="ORG-xxxx",
            api_key="lysk-xxxxxxxxxxx",
            endpoint="https://api.lybic.cn/",
       )
     ) as client:
           computer_use = ComputerUse(client)
           parsed_result = await computer_use.parse_llm_output(
               model_type="ui-tars",
               llm_output="""Thought: The task requires double-left-clicking the "images" folder. In the File Explorer window, the "images" folder is visible under the Desktop directory. The target element is the folder named "images" with a yellow folder icon. Double-left-clicking this folder will open it.
     
           Next action: Left - double - click on the "images" folder icon located in the File Explorer window, under the Desktop directory, with the name "images" and yellow folder icon.
           Action: left_double(point='<point>213 257</point>')"""
           )
           actions = parsed_result.actions
           if actions:
               sandbox = Sandbox(client)
               # Using DTO
               response = await sandbox.execute_sandbox_action(
                   sandbox_id="SBX-xxxx",
                   data=dto.ExecuteSandboxActionDto(action=actions[0])
               )
               print(response)
               # Using keyword arguments
               response_2 = await sandbox.execute_sandbox_action(
                   sandbox_id="SBX-xxxx",
                   action=actions[0]
               )
               print(response_2)
   if __name__ == "__main__":
       asyncio.run(main())
   ```

8. Upload files to a sandbox (MinIO end-to-end example)

   **Note:** The actual process of "uploading files to the sandbox" is as follows: the user first uploads a local file to an object storage service (like MinIO) to generate an accessible URL. Then, the sandbox downloads the file from this URL and saves it to the specified `localPath`. In other words: **User Uploads → Object Storage → Sandbox Downloads**.

   **Workflow:**
   ```mermaid
   sequenceDiagram
       participant User
       participant MinIO as Object Storage
       participant Sandbox

       User->>MinIO: Upload local file
       MinIO-->>User: Generate presigned URL
       User->>Sandbox: Call upload_files() with URL
       Sandbox->>MinIO: Download file from URL
       MinIO-->>Sandbox: File content
       Sandbox->>Sandbox: Save file to localPath
   ```

   **Prerequisites:**
   - Install minio SDK: `pip install minio`
   - You already have a MinIO instance and bucket (e.g. `agent-data`)

   **Complete workflow:**
   1. Upload local file to MinIO using MinIO SDK
   2. Generate a presigned GET URL for the uploaded object
   3. Call Lybic `sandbox.upload_files()` with the presigned URL
   4. Sandbox downloads the file from the URL and saves it to the specified path

   ```python
   import asyncio
   from minio import Minio
   from lybic import Sandbox, LybicClient, LybicAuth

   # MinIO configuration
   MINIO_ENDPOINT = 'play.min.io'  # Replace with your MinIO endpoint
   ACCESS_KEY = 'YOUR_MINIO_ACCESS_KEY'
   SECRET_KEY = 'YOUR_MINIO_SECRET_KEY'
   USE_SECURE = True
   BUCKET = 'agent-data'

   # File configuration
   LOCAL_FILE_PATH = './local_input.txt'  # Local file to upload
   OBJECT_NAME = 'uploads/input.txt'  # Object key in MinIO
   SANDBOX_PATH = '/home/agent/data/input.txt'  # Destination path in sandbox

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
       presigned_url = minio_client.presigned_get_object(BUCKET, OBJECT_NAME, expires=3600)
       print(f"Generated presigned URL: {presigned_url}")
       
       # Step 3: Use Lybic SDK to transfer file to sandbox
       async with LybicClient(LybicAuth(org_id='ORG-xxxx', api_key='lysk-xxxxxxxxxxx')) as client:
           sandbox = Sandbox(client)
           
           # Call upload_files - sandbox will download from the presigned URL
           response = await sandbox.upload_files(
               'SBX-xxxx',  # Your sandbox ID
               files=[{
                   'localPath': SANDBOX_PATH,
                   'putUrl': presigned_url  # URL for sandbox to download from
               }]
           )
           
           print("Upload result:", response)
           for result in response.results:
               if result.success:
                   print(f"✓ File successfully transferred to sandbox: {result.localPath}")
               else:
                   print(f"✗ Failed to transfer file: {result.error}")

   if __name__ == '__main__':
       asyncio.run(upload_file_to_sandbox())
   ```

   **Advanced: Using Multipart Upload Configuration**

   For large files, you can use MinIO's multipart upload with POST policy:

   ```python
   from minio import Minio, PostPolicy
   from datetime import datetime, timedelta
   from lybic import dto

   minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=USE_SECURE)
   
   # Create POST policy for multipart upload
   policy = PostPolicy()
   policy.set_bucket(BUCKET)
   policy.set_key('uploads/large_file.bin')
   policy.set_expires(datetime.utcnow() + timedelta(hours=1))
   
   form_data = minio_client.presigned_post_policy(policy)
   
   # Configure multipart upload
   multipart_config = dto.MultipartUploadConfig(
       url=form_data['url'],
       formFields={k: v for k, v in form_data.items() if k != 'url'},
       fileFieldName='file'
   )
   
   # Use in FileUploadItem
   upload_item = dto.FileUploadItem(
       localPath='/home/agent/data/large_file.bin',
       putUrl=form_data['url'],
       multipartUpload=multipart_config
   )
   ```

9. Download files from a sandbox (MinIO end-to-end example)

   **Note:** The actual process of "downloading files from the sandbox" is as follows: the user first generates a presigned PUT URL using the MinIO SDK. The sandbox then uploads its local file to this URL. Finally, the user downloads the file from MinIO to their local machine. In other words: **Sandbox Uploads → Object Storage → User Downloads**.

   **Workflow:**
   ```mermaid
   sequenceDiagram
       participant User
       participant MinIO as Object Storage
       participant Sandbox

       User->>MinIO: Request presigned PUT URL
       MinIO-->>User: Generate presigned PUT URL
       User->>Sandbox: Call download_files() with URL
       Sandbox->>MinIO: Upload file to presigned URL
       MinIO-->>Sandbox: Upload success
       User->>MinIO: Download file
       MinIO-->>User: File content
   ```

   **Complete workflow:**
   1. Generate a presigned PUT URL using MinIO SDK
   2. Call Lybic `sandbox.download_files()` with the presigned PUT URL
   3. Sandbox uploads its local file to the presigned URL
   4. Download the file from MinIO to local machine

   ```python
   import asyncio
   from minio import Minio
   from lybic import Sandbox, LybicClient, LybicAuth

   # MinIO configuration
   MINIO_ENDPOINT = 'play.min.io'
   ACCESS_KEY = 'YOUR_MINIO_ACCESS_KEY'
   SECRET_KEY = 'YOUR_MINIO_SECRET_KEY'
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
       presigned_put_url = minio_client.presigned_put_object(BUCKET, OBJECT_NAME, expires=3600)
       print(f"Generated presigned PUT URL: {presigned_put_url}")
       
       # Step 2: Use Lybic SDK to transfer file from sandbox
       async with LybicClient(LybicAuth(org_id='ORG-xxxx', api_key='lysk-xxxxxxxxxxx')) as client:
           sandbox = Sandbox(client)
           
           # Call download_files - sandbox will upload to the presigned URL
           response = await sandbox.download_files(
               'SBX-xxxx',  # Your sandbox ID
               files=[{
                   'url': presigned_put_url,  # URL for sandbox to upload to
                   'localPath': SANDBOX_FILE_PATH
               }]
           )
           
           print("Download result:", response)
           for result in response.results:
               if result.success:
                   print(f"✓ File successfully transferred from sandbox: {result.localPath}")
               else:
                   print(f"✗ Failed to transfer file: {result.error}")
       
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

   **Complete example with file verification:**

   ```python
   import asyncio
   from minio import Minio
   from lybic import Sandbox, LybicClient, LybicAuth

   async def download_and_verify():
       minio_client = Minio('play.min.io', 'YOUR_ACCESS_KEY', 'YOUR_SECRET_KEY', secure=True)
       
       # Generate presigned PUT URL
       put_url = minio_client.presigned_put_object('agent-data', 'results/report.json', expires=3600)
       
       # Trigger sandbox to upload file to MinIO
       async with LybicClient(LybicAuth(org_id='ORG-xxxx', api_key='lysk-xxxxxxxxxxx')) as client:
           sandbox = Sandbox(client)
           resp = await sandbox.download_files(
               'SBX-xxxx',
               files=[{
                   'url': put_url,
                   'localPath': '/home/agent/output/report.json'
               }]
           )
           
           if resp.results[0].success:
               print("File uploaded from sandbox to MinIO successfully")
           else:
               print(f"Upload failed: {resp.results[0].error}")
               return
       
       # Download from MinIO to local
       minio_client.fget_object('agent-data', 'results/report.json', './local_report.json')
       print("File downloaded to local machine")
       
       # Verify file size
       obj_stat = minio_client.stat_object('agent-data', 'results/report.json')
       print(f"File size: {obj_stat.size} bytes")

   if __name__ == '__main__':
       asyncio.run(download_and_verify())
   ```

   **Advanced: Using POST policy for multipart upload from sandbox**

   ```python
   from minio import Minio, PostPolicy
   from datetime import datetime, timedelta

   minio_client = Minio(MINIO_ENDPOINT, ACCESS_KEY, SECRET_KEY, secure=USE_SECURE)
   
   # Create POST policy
   policy = PostPolicy()
   policy.set_bucket(BUCKET)
   policy.set_key('downloads/large_output.bin')
   policy.set_expires(datetime.utcnow() + timedelta(minutes=30))
   
   form_data = minio_client.presigned_post_policy(policy)
   
   # Use with sandbox.download_files
   # Note: form_data contains both 'url' and additional form fields
   response = await sandbox.download_files(
       'SBX-xxxx',
       files=[{
           'url': form_data['url'],
           'localPath': '/home/agent/data/large_output.bin',
           'headers': {k: v for k, v in form_data.items() if k != 'url'}
       }]
   )
   ```

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
    from lybic import dto, Sandbox, LybicClient, LybicAuth

    async def run_process_example():
        async with LybicClient(LybicAuth(org_id='ORG-xxxx', api_key='lysk-xxxxxxxxxxx')) as client:
            sandbox = Sandbox(client)
            
            # Example 1: Simple command
            result = await sandbox.execute_process(
                'SBX-xxxx',
                executable='/bin/echo',
                args=['Hello', 'World']
            )
            print(f"Exit code: {result.exitCode}")
            stdout = base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')
            print(f"Output: {stdout}")
            
            # Example 2: Python script with stdin
            stdin_data = base64.b64encode(b"print('Hello from stdin')\\n").decode()
            proc_req = dto.SandboxProcessRequestDto(
                executable='/usr/bin/python3',
                args=['-c', 'import sys; exec(sys.stdin.read())'],
                workingDirectory='/home/agent',
                stdinBase64=stdin_data
            )
            result = await sandbox.execute_process('SBX-xxxx', data=proc_req)
            print(f"Exit: {result.exitCode}")
            print(f"STDOUT: {base64.b64decode(result.stdoutBase64 or '').decode(errors='ignore')}")
            print(f"STDERR: {base64.b64decode(result.stderrBase64 or '').decode(errors='ignore')}")

    if __name__ == '__main__':
        asyncio.run(run_process_example())
    ```
