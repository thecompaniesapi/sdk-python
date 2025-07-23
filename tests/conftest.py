import pytest
from src.thecompaniesapi import Client, HttpClient


@pytest.fixture
def http_client():
    """Fixture providing an HttpClient instance for testing."""
    return HttpClient(api_token="test-token")


@pytest.fixture
def http_client_with_visitor():
    """Fixture providing an HttpClient with visitor ID for testing."""
    return HttpClient(api_token="test-token", visitor_id="test-visitor-123")


@pytest.fixture
def client():
    """Fixture providing a Client instance for testing."""
    return Client(api_token="test-token")


@pytest.fixture
def custom_client():
    """Fixture providing a Client with custom configuration for testing."""
    return Client(
        api_token="custom-token",
        api_url="https://custom.api.com",
        visitor_id="custom-visitor",
        timeout=120
    ) 
