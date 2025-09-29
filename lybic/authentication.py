# -*- coding: UTF-8 -*-
#
# Copyright (c) 2019-2025   Beijing Tingyu Technology Co., Ltd.
# Copyright (c) 2025        Lybic Development Team <team@lybic.ai, lybic@tingyutech.com>
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

"""authentication.py holds the authentication for Lybic API."""
import os


class LybicAuth:
    """LybicAuth holds the authentication for Lybic API."""

    org_id:  str # Your organization ID
    api_key: str # Your API key
    endpoint: str # Your API endpoint
    headers: dict # Extra headers if needed

    agent_service_endpoint: str

    def __init__(self,
                 org_id: str = os.getenv("LYBIC_ORG_ID"),
                 api_key: str = os.getenv("LYBIC_API_KEY"),
                 endpoint: str = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.cn"),
                 agent_service_endpoint: str = os.getenv("LYBIC_AGENT_SERVICE_ENDPOINT", "https://agent.lybic.cn"),
                 extra_headers: dict = None,
                 ):
        """
        Initializes the LybicAuth instance.

        :param org_id: Your organization ID. Defaults to the `LYBIC_ORG_ID` environment variable. Required.
        :param api_key: Your API key. Defaults to the `LYBIC_API_KEY` environment variable. Required unless `x-trial-session-token` is in `extra_headers`.
        :param endpoint: The API endpoint. Defaults to the `LYBIC_API_ENDPOINT` environment variable or "https://api.lybic.cn". Required.
        :param extra_headers: A dictionary of extra headers to include in requests.
        """
        self.headers = {}
        if extra_headers:
            self.headers.update(extra_headers)

        # if x-trial-session-token is provided, use it instead of api_key
        if not (extra_headers and 'x-trial-session-token' in extra_headers):
            assert api_key, "LYBIC_API_KEY is required when x-trial-session-token is not provided"
            self.headers["x-api-key"] = api_key
        self.api_key = api_key

        self.endpoint = endpoint.rstrip('/')
        self.agent_service_endpoint = agent_service_endpoint.rstrip('/')

        self.org_id = org_id
        self.headers["Content-Type"] = "application/json"
