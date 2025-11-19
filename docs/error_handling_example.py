#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
Example demonstrating the new custom error handling in Lybic SDK.

The SDK now provides user-friendly exceptions for API errors instead of raw HTTP errors.
"""
import asyncio
from lybic import LybicClient, LybicAPIError, LybicInternalError


async def example_basic_error_handling():
    """Basic example of handling Lybic API errors."""
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


async def example_structured_api_error():
    """
    Example of structured API error response.
    
    When the API returns a structured error like:
    {"code": "nomos.partner.NO_ROOMS_AVAILABLE", "message": "No rooms available"}
    
    The SDK will raise LybicAPIError with:
    - message: "No rooms available"
    - code: "nomos.partner.NO_ROOMS_AVAILABLE"
    - status_code: HTTP status code (e.g., 400, 404, 500)
    """
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


async def example_internal_error():
    """
    Example of internal server error from reverse proxy.
    
    When a 5xx error occurs at the reverse proxy level and returns HTML
    instead of JSON, the SDK will raise LybicInternalError with:
    - message: "internal error occur"
    - status_code: HTTP status code (e.g., 500, 502, 503)
    """
    async with LybicClient() as client:
        try:
            result = await client.request("GET", "/api/endpoint")
        except LybicInternalError as e:
            print(f"Internal error: {e.message}")  # "internal error occur"
            print(f"Status code: {e.status_code}")


async def example_catch_all_lybic_errors():
    """
    Example of catching all Lybic-specific errors.
    
    You can catch LybicError to handle all SDK-specific errors,
    or catch specific exceptions for more granular handling.
    """
    from lybic import LybicError
    
    async with LybicClient() as client:
        try:
            result = await client.request("GET", "/api/endpoint")
        except LybicError as e:
            # This catches both LybicAPIError and LybicInternalError
            print(f"Lybic SDK error: {e.message}")
            print(f"Status code: {e.status_code}")


# Note: These examples will fail without valid credentials, but demonstrate
# how to use the error handling in your actual code.

if __name__ == "__main__":
    print("Lybic SDK Error Handling Examples")
    print("=" * 50)
    print("\nThese examples demonstrate how to handle different error types.")
    print("Run with valid credentials to see actual error responses.\n")
