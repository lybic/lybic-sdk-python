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

"""exceptions.py provides custom exceptions for Lybic API."""
from typing import Optional


class LybicError(Exception):
    """Base exception class for all Lybic SDK errors."""

    def __init__(self, message: str, status_code: Optional[int] = None):
        """
        Initialize LybicError.

        :param message: Error message
        :param status_code: HTTP status code if applicable
        """
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class LybicAPIError(LybicError):
    """Exception raised for API errors with structured error responses.
    
    This exception is raised when the API returns an error response with
    a structured format containing 'code' and 'message' fields.
    
    Example response:
    {"code": "nomos.partner.NO_ROOMS_AVAILABLE", "message": "No rooms available"}
    """

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        status_code: Optional[int] = None,
    ):
        """
        Initialize LybicAPIError.

        :param message: Error message from API response
        :param code: Error code from API response
        :param status_code: HTTP status code
        """
        self.code = code
        super().__init__(message, status_code)

    def __str__(self) -> str:
        """Return string representation of the error."""
        if self.code:
            return f"{self.message} (code: {self.code})"
        return self.message


class LybicInternalError(LybicError):
    """Exception raised for internal server errors (5xx) from reverse proxy.
    
    This exception is raised when a 5xx error occurs at the reverse proxy level,
    typically returning an HTML error page instead of a JSON response.
    """

    def __init__(self, status_code: int = 500):
        """
        Initialize LybicInternalError.

        :param status_code: HTTP status code (5xx)
        """
        super().__init__("internal error occur", status_code)
