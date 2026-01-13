# Api BreakChange from 0.x to 1.x

Starting from version 1.0, we have deprecated the following APIs. 
If you have updated to SDK version >= 0.12 and are not receiving deprecation warnings when calling these APIs, 
you can safely update to Lybic SDK >= 1.0 without any additional work.

---

1. `lybic.lmcp` has been removed.

    `lybic.lmcp` was the interface used by users to call the Lybic MCP server via the MCP protocol and manage MCP server instances.
    If you were previously using `lybic.lmcp.MCP`, you need to update the import to `lybic.mcp.Mcp` or directly use `LybicClient.mcp`.

2. `lybic.tools.ComputerUse`

    `parse_model_output()` has been replaced by the new interface `parse_llm_output()`, which adds more model output text 
     parsing and unifies the API path.
    
    `execute_computer_use_action()` has been replaced by the `LybicClient.sandbox.execute_sandbox_action()` API. 
    The new interface does not distinguish whether the action is a computer-use specific action, thus improving generality. 
    You only need to replace the original call from `computer_use.execute_computer_use_action()` to `LybicClient.sandbox.execute_sandbox_action()`.

3. `lybic.pyautogui.Pyautogui`
   
    In version 0.x, this module could execute synchronous code in an asynchronous context without blocking warnings, 
    which caused confusion for users. From version 1.0, this module has been moved to `lybic_sync.pyautogui.PyautoguiSync`, 
    indicating that this module is a synchronous-only module, and executing it in an asynchronous context may cause the event 
    loop to be blocked. However, we have not removed this API; we have only performed a redirection. We recommend that you
    update your import to `lybic_sync.pyautogui.PyautoguiSync` to help developers confirm the impact of this module on their 
    business code.
