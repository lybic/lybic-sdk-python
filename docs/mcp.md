# Mcp example:

To use the `Mcp` client, you must first install it with the optional dependencies:
```bash
pip install 'lybic[mcp]'
```

You can use the `MCP(Model Context Protocol)` to execute action via `lybic.Mcp`.

```python
class Mcp:
    async def call_tool_async(self,
                              mcp_server_id: str,
                              tool_name: str = "computer-use",
                              tool_args: dict = None):
        """
        Call a tool on mcp server

        :param mcp_server_id:
        :param tool_name:
        :param tool_args:
        :return tool_result:
        """
``` 

## method call_tool_async

### args: mcp_server_id: mcp server id

You can get it from the website or the SDK.

- Website:
1. Open the dashboard of the lybic web app.
2. Find the `MCP Servers` on the left side.
3. You will see the mcp server id.

- SDK:
```python
import asyncio
from lybic import Mcp

mcp = Mcp(client)

list_result =  asyncio.run(mcp.list())

for mcp_server in list_result.root:
    print(mcp_server.id)
```

### args: tool_name: tool name

It is the name of the MCP tool you want to run.

### args: tool_args: a dictionary of tool args

such as:

```python
args={
   "action": "click",
   "coordinate": [{x}, {y}],
   "text": "{','.join(hold_keys) if hold_keys else None}"
}
```

### Return val of MCP

tool_result.content

## support arg actions:

Full actions please refer to

- [tools.json](tools.json)
- [OpenAI](https://platform.openai.com/docs/guides/tools-computer-use#page-top)
- [Anthropic](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool#computer-tool)

```
action 
- click
- rightClick - （Computer only）
- longPress - （Phone only)
- doubleClick - （Computer only）
- middleClick - （Computer only）
- cursorPosition - （Computer only）
- leftClickDrag - 
- keyPress - 
- move - 
- screenShot - 
- scroll - 
- type - 
- wait - 
coordinate 
The target coordinates of the operation, [x, y]; only valid for click and move operations.
startCoordinate: Starting coordinates
The starting coordinates of the operation, [x, y]; only valid for drag operations.
text: The text to be entered; only valid for text input operations.
scrollDistance: Scroll distance
The distance to scroll; only valid for scroll operations.
Properties:
- display_width: Display width.
- display_height: Display height.
- environment: Windows, Linux, browser, Android

File Edit tools:
command:
- view
- create
- str_replace
- insert
- undo_edit
file_text: File content: The contents of the created file.
insert_line: Insert content: The line to be inserted.
new_str: The new string to be replaced when replacing.
old_str: The old string to be replaced when replacing.
path: The file path to be edited.
view_range: The range to be viewed.
```

## examples:

1. Get the screenshot via MCP

    ```python
    import asyncio
    import base64
    from io import BytesIO
    from PIL import Image
    from lybic import LybicClient, Mcp
    
    async def main():
        async with LybicClient() as client:
            mcp = Mcp(client)
            result = await mcp.call_tool_async(mcp_server_id='server_id',tool_args={"action": "screenShot"})
            img_b64 = result.content[0].data
            img_bytes = base64.b64decode(img_b64)
            i = Image.open(BytesIO(img_bytes))
            i.show()
            print(result)
    if __name__ == '__main__':
        asyncio.run(main())
    ```

2. Input text to textbox:

    ```python
    import asyncio
    from lybic import LybicClient, Mcp
    
    async def main():
        async with LybicClient() as client:
            mcp = Mcp(client)
            result = await mcp.call_tool_async(mcp_server_id='server_id',tool_args={"action": "type", "text": "This is a English text,and 这是一个中文文本"})
            print(result)
    if __name__ == '__main__':
        asyncio.run(main())
    ```
   
3. Click a button:

    ```python
    import asyncio
    from lybic import LybicClient, Mcp
    
    async def main():
        async with LybicClient() as client:
            mcp = Mcp(client)
            result = await mcp.call_tool_async(mcp_server_id='server_id', tool_args={"action": "click", "coordinate": [100, 200]})
            print(result)
    if __name__ == '__main__':
        asyncio.run(main()) 
   ```
   
