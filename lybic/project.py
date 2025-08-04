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

"""project.py provides the Project manager ability to use"""
from typing import overload

from lybic import dto
from lybic.lybic import LybicClient

class Project:
    """
    Projects class are used to organize Projects.
    """
    def __init__(self, client: LybicClient):
        self.client = client

    async def list(self) -> dto.ListProjectsResponseDto:
        """
        List all projects in the organization.
        """
        self.client.logger.debug("Listing projects request")
        response = await self.client.request("GET", f"/api/orgs/{self.client.org_id}/projects")
        self.client.logger.debug("Listing projects response: %s", response.text)
        return dto.ListProjectsResponseDto.model_validate_json(response.text)

    @overload
    async def create(self, data: dto.CreateProjectDto) -> dto.SingleProjectResponseDto: ...

    @overload
    async def create(self, **kwargs) -> dto.SingleProjectResponseDto: ...

    async def create(self, *args, **kwargs) -> dto.SingleProjectResponseDto:
        """
        Create a new project.
        """
        if args and isinstance(args[0], dto.CreateProjectDto):
            data = args[0]
        else:
            data = dto.CreateProjectDto(**kwargs)
        self.client.logger.debug("Creating project request with data: %s", data)
        response = await self.client.request(
            "POST",
            f"/api/orgs/{self.client.org_id}/projects", json=data.model_dump())
        self.client.logger.debug("Create project response: %s", response.text)
        return dto.SingleProjectResponseDto.model_validate_json(response.text)

    async def delete(self, project_id: str) -> None:
        """
        Delete a project.
        """
        self.client.logger.debug("Deleting project request with project_id: %s", project_id)
        await self.client.request("DELETE", f"/api/orgs/{self.client.org_id}/projects/{project_id}")
