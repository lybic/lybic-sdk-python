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
    apikey: str # Your API key
    endpoint: str # Your API endpoint
    headers: dict # Extra headers if needed

    def __init__(self,
                 org_id: str = os.getenv("LYBIC_ORG_ID"),
                 api_key: str = os.getenv("LYBIC_API_KEY"),
                 endpoint: str = os.getenv("LYBIC_API_ENDPOINT", "https://api.lybic.cn"),
                 extra_headers: dict = None,
                 ):
        """
        Init lybic auth with org_id, api_key and endpoint

        :param org_id:
        :param api_key:
        :param endpoint:
        """
        assert org_id, "LYBIC_ORG_ID is required"
        assert endpoint, "LYBIC_API_ENDPOINT is required"

        self.headers = {}
        if extra_headers:
            self.headers.update(extra_headers)

        # if x-trial-session-token is provided, use it instead of api_key
        if not (extra_headers and 'x-trial-session-token' in extra_headers):
            assert api_key, "LYBIC_API_KEY is required when x-trial-session-token is not provided"
            self.headers["x-api-key"] = api_key
        self.apikey = api_key

        if endpoint.endswith("/"):
            self.endpoint = endpoint[:-1]
        else:
            self.endpoint = endpoint

        self.org_id = org_id
        self.headers["Content-Type"] = "application/json"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
