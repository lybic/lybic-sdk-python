#!/usr/bin/env python3
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
"""This file is lybic SDK E2E Test scripts"""
import asyncio
from lybic import (Project,
                   MCP,
                   Sandbox,
                   ComputerUse,
                   LybicClient,
                   Stats, Pyautogui)

async def test_stats(client:LybicClient):
    """
    Test Restful API Class: Stats
    :param client:
    :return:
    """
    stats = Stats(client)
    result =  await stats.get()
    print(result)

async def test_project(client:LybicClient):
    """
    Test Restful API Class: Project
    :param client:
    :return:
    """
    project = Project(client)
    print("Test List Project:",await project.list())
    print("Test Create Project:",)
    result = await project.create(name='test_project')
    print("Result:",result)
    print("Test Delete Project")
    await project.delete(result.id)

async def test_sandbox(client:LybicClient):
    """
    Test Restful API Class: Sandbox
    :param client:
    :return:
    """
    await Project(client).create(name='test_sandbox')
    sandbox = Sandbox(client)

    print("Test List Sandbox:",await sandbox.list())
    print("Test Create Sandbox:",await sandbox.create(name="test_sandbox"))

    print("Test Get Sandbox:")
    result = await sandbox.get("test_sandbox")
    print(result)

    print("Test Delete Sandbox",await sandbox.delete(result.sandbox.id))
    print("Test Get Sandbox preview info",await sandbox.preview(result.sandbox.id))
    print("Test Extend Sandbox",await sandbox.extend_life(result.sandbox.id))
    print("Test Get Sandbox connection details",await sandbox.get_connection_details(result.sandbox.id))
    # print("Test Get Sandbox screenshot",await sandbox.get_screenshot(result.sandbox.id))

async def test_mcp(client:LybicClient):
    """
    Test Restful API Class: MCP
    :param client:
    :return:
    """
    await Sandbox(client).create(name='test_mcp')
    mcp = MCP(client)

    print("Test List MCP:",await mcp.list())
    print("Test Create MCP:",await mcp.create(name="test_mcp"))
    print("Test Delete MCP",await mcp.delete("test_mcp"))
    print("Test Set MCP Sandbox",await mcp.set_sandbox("test_mcp","test_sandbox"))
    # print("Test Call MCP Tool",await mcp.call_tool_async("test_mcp"))

async def test_computer_use(client:LybicClient):
    """
    Test Restful API Class: ComputerUse
    :param client:
    :return:
    """
    await Sandbox(client).create(name='test_computer_use')
    computer_use = ComputerUse(client)

    print("Test parse model output:")
    action = await computer_use.parse_model_output(
        model="seed",
        textContent="""Thought: The user wants to open the Chrome app. The screenshot shows the Google Chrome icon on the desktop. I should double-click the Google Chrome icon to open the app.
    Action: left_double(point='<point>10 10</point>')"""
    )
    print("ActionResult:",action)

    sandbox = Sandbox(client)
    print("Execute computer use action:",await sandbox.execute_computer_use_action(
        sandbox_id='test_computer_use',
        action=action.actions[0]
    ))


# pylint: disable=eval-used,fixme
def test_pyautogui(client:LybicClient):
    """
    Test Pyautogui
    :param client:
    :return:
    """
    pyautogui = Pyautogui(client, sandbox_id='test_pyautogui')

    print("Test pyautogui.click without position arguments.")
    pyautogui.click()
    print("Test pyautogui.click with position arguments.")
    pyautogui.click(10, 10)
    print("Test pyautogui.moveTo.")
    pyautogui.moveTo(10, 10)
    print("Test pyautogui.move.")
    pyautogui.move(10, 10)
    print("Test pyautogui.press.")
    pyautogui.press('1')
    print("Test pyautogui.write.")
    pyautogui.write('Hello world!')
    print("Test pyautogui.hotkey.")
    pyautogui.hotkey('ctrl', 'c')

    print("Test Pyautogui Expression Execution")
    expression = 'pyautogui.click(x=1443, y=343)'
    eval(expression)

    pyautogui.close()


async def restful_test() -> None:
    """
    Core restful api test
    """
    async with LybicClient() as client:
        tasks = [
            asyncio.create_task(test_stats(client)),
            asyncio.create_task(test_project(client)),
            asyncio.create_task(test_sandbox(client)),
            asyncio.create_task(test_mcp(client)),
            asyncio.create_task(test_computer_use(client)),
            asyncio.create_task(Sandbox(client).create(name='test_pyautogui'))
        ]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # test restful api(asynchronize_test)
    asyncio.run(restful_test())
    # test pyautogui(synchronize_test)
    test_pyautogui(LybicClient())
