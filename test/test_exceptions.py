#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Test custom exception handling for Lybic SDK."""
import asyncio
import json
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from lybic import LybicClient, LybicAPIError, LybicInternalError, LybicError

@pytest.mark.asyncio
async def test_api_error_with_structured_response():
    """Test that structured API error responses are converted to LybicAPIError."""
    # Initialize with dummy credentials
    async with LybicClient(org_id="test_org", api_key="test_key") as client:
        # Mock response with structured error
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "code": "nomos.partner.NO_ROOMS_AVAILABLE",
            "message": "No rooms available"
        }

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Bad Request",
            request=Mock(spec=httpx.Request),
            response=mock_response
        )

        # Mock the client request to raise HTTPStatusError
        with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = error

            try:
                await client.request("GET", "/test")
                assert False, "Expected LybicAPIError to be raised"
            except LybicAPIError as e:
                assert e.message == "No rooms available"
                assert e.code == "nomos.partner.NO_ROOMS_AVAILABLE"
                assert e.status_code == 400
                assert "No rooms available" in str(e)
                assert "nomos.partner.NO_ROOMS_AVAILABLE" in str(e)


@pytest.mark.asyncio
async def test_internal_error_from_reverse_proxy():
    """Test that 5xx errors without JSON response are converted to LybicInternalError."""
    async with LybicClient(org_id="test_org", api_key="test_key") as client:
        # Mock response with HTML error page (from reverse proxy)
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 502
        mock_response.json.side_effect = json.JSONDecodeError("msg", "doc", 0)

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Bad Gateway",
            request=Mock(spec=httpx.Request),
            response=mock_response
        )

        # Mock the client request to raise HTTPStatusError
        with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = error

            try:
                await client.request("GET", "/test")
                assert False, "Expected LybicInternalError to be raised"
            except LybicInternalError as e:
                assert e.message == "internal error occur"
                assert e.status_code == 502
                assert str(e) == "internal error occur"


@pytest.mark.asyncio
async def test_5xx_error_with_structured_response():
    """Test that 5xx errors with structured JSON response are converted to LybicAPIError."""
    async with LybicClient(org_id="test_org", api_key="test_key") as client:
        # Mock response with structured error
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.json.return_value = {
            "code": "internal.server.error",
            "message": "Database connection failed"
        }

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Internal Server Error",
            request=Mock(spec=httpx.Request),
            response=mock_response
        )

        # Mock the client request to raise HTTPStatusError
        with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = error

            try:
                await client.request("GET", "/test")
                assert False, "Expected LybicAPIError to be raised"
            except LybicAPIError as e:
                assert e.message == "Database connection failed"
                assert e.code == "internal.server.error"
                assert e.status_code == 500


@pytest.mark.asyncio
async def test_exception_without_code():
    """Test that API errors without code field still work."""
    async with LybicClient(org_id="test_org", api_key="test_key") as client:
        # Mock response with message but no code
        mock_response = Mock(spec=httpx.Response)
        mock_response.status_code = 400
        mock_response.json.return_value = {
            "message": "Invalid request"
        }

        # Create HTTPStatusError
        error = httpx.HTTPStatusError(
            "Bad Request",
            request=Mock(spec=httpx.Request),
            response=mock_response
        )

        # Mock the client request to raise HTTPStatusError
        with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = error

            try:
                await client.request("GET", "/test")
                assert False, "Expected LybicAPIError to be raised"
            except LybicAPIError as e:
                assert e.message == "Invalid request"
                assert e.code is None
                assert e.status_code == 400
                assert str(e) == "Invalid request"


@pytest.mark.asyncio
async def test_network_error_passthrough():
    """Test that network errors are passed through as-is."""
    async with LybicClient(org_id="test_org", api_key="test_key") as client:
        # Create a network error
        error = httpx.RequestError("Connection failed")

        # Mock the client request to raise RequestError
        with patch.object(client.client, 'request', new_callable=AsyncMock) as mock_request:
            mock_request.side_effect = error

            try:
                await client.request("GET", "/test")
                assert False, "Expected httpx.RequestError to be raised"
            except httpx.RequestError:
                pass  # Expected


def test_exception_import():
    """Test that exceptions can be imported from lybic module."""
    # Test creating instances
    base_error = LybicError("test message", 500)
    assert base_error.message == "test message"
    assert base_error.status_code == 500

    api_error = LybicAPIError("API error", "error.code", 400)
    assert api_error.message == "API error"
    assert api_error.code == "error.code"
    assert api_error.status_code == 400

    internal_error = LybicInternalError(502)
    assert internal_error.message == "internal error occur"
    assert internal_error.status_code == 502


if __name__ == "__main__":
    # Run tests
    print("Testing exception handling...")
    asyncio.run(test_api_error_with_structured_response())
    print("✓ API error with structured response")

    asyncio.run(test_internal_error_from_reverse_proxy())
    print("✓ Internal error from reverse proxy")

    asyncio.run(test_5xx_error_with_structured_response())
    print("✓ 5xx error with structured response")

    asyncio.run(test_exception_without_code())
    print("✓ Exception without code field")

    asyncio.run(test_network_error_passthrough())
    print("✓ Network error passthrough")

    test_exception_import()
    print("✓ Exception import")

    print("\n✓ All exception handling tests passed!\n")
