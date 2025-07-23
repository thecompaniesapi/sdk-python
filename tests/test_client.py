import json
import pytest
import responses
from unittest.mock import Mock, patch

from src.thecompaniesapi import Client, HttpClient, ApiError


@pytest.mark.unit
class TestHttpClient:
    """Test the HttpClient class functionality."""
    
    def test_init_default_params(self):
        """Test HttpClient initialization with default parameters."""
        client = HttpClient(api_token="test-token")
        
        assert client.api_token == "test-token"
        assert client.api_url == "https://api.thecompaniesapi.com"
        assert client.visitor_id is None
        assert client.timeout == 300
    
    def test_init_custom_params(self):
        """Test HttpClient initialization with custom parameters."""
        client = HttpClient(
            api_token="custom-token",
            api_url="https://custom.api.com",
            visitor_id="visitor-123",
            timeout=60
        )
        
        assert client.api_token == "custom-token"
        assert client.api_url == "https://custom.api.com"
        assert client.visitor_id == "visitor-123"
        assert client.timeout == 60
    
    def test_setup_default_headers(self):
        """Test that default headers are set correctly."""
        client = HttpClient(api_token="test-token", visitor_id="visitor-123")
        
        headers = client.session.headers
        assert headers['Content-Type'] == 'application/json'
        assert headers['Accept'] == 'application/json'
        assert headers['Authorization'] == 'Basic test-token'
        assert headers['Tca-Visitor-Id'] == 'visitor-123'
        assert 'thecompaniesapi-python-sdk' in headers['User-Agent']
    
    def test_setup_headers_no_visitor_id(self):
        """Test headers when no visitor ID is provided."""
        client = HttpClient(api_token="test-token")
        
        headers = client.session.headers
        assert 'Tca-Visitor-Id' not in headers  # Should not be present when not provided
    
    def test_serialize_query_params(self):
        """Test query parameter serialization."""
        client = HttpClient(api_token="test-token")
        
        params = {
            "string": "hello",
            "number": 42,
            "boolean_true": True,
            "boolean_false": False,
            "list": ["item1", "item2"],
            "dict": {"key": "value", "nested": {"deep": "data"}},
            "none_value": None
        }
        
        result = client._serialize_query_params(params)
        
        assert result["string"] == "hello"
        assert result["number"] == "42"
        assert result["boolean_true"] == "true"
        assert result["boolean_false"] == "false"
        assert result["list"] == '%5B%22item1%22%2C%22item2%22%5D'  # URL-encoded ["item1","item2"]
        assert result["dict"] == '%7B%22key%22%3A%22value%22%2C%22nested%22%3A%7B%22deep%22%3A%22data%22%7D%7D'  # URL-encoded {"key":"value","nested":{"deep":"data"}}
        assert "none_value" not in result
    
    def test_prepare_url(self):
        """Test URL preparation."""
        client = HttpClient(api_token="test-token", api_url="https://api.example.com")
        
        # Test with leading slash
        assert client._prepare_url("/v2/health") == "https://api.example.com/v2/health"
        
        # Test without leading slash
        assert client._prepare_url("v2/health") == "https://api.example.com/v2/health"
        
        # Test with complex path
        assert client._prepare_url("companies/search") == "https://api.example.com/companies/search"
    
    @responses.activate
    def test_get_request_success(self):
        """Test successful GET request."""
        responses.add(
            responses.GET,
            "https://api.thecompaniesapi.com/v2/health",
            json={"status": "ok"},
            status=200
        )
        
        client = HttpClient(api_token="test-token")
        result = client.get("/v2/health")
        
        assert result == {"status": "ok"}
    
    @responses.activate
    def test_get_request_with_params(self):
        """Test GET request with query parameters."""
        responses.add(
            responses.GET,
            "https://api.thecompaniesapi.com/v2/companies",
            json={"data": []},
            status=200
        )
        
        client = HttpClient(api_token="test-token")
        params = {"size": 10, "query": ["test"]}
        result = client.get("/v2/companies", params=params)
        
        # Check that the request was made with serialized params
        assert len(responses.calls) == 1
        request_url = responses.calls[0].request.url
        assert "size=10" in request_url
        assert "query=%255B%2522test%2522%255D" in request_url  # Double URL-encoded JSON (our encoding + requests encoding)
    
    @responses.activate
    def test_post_request_success(self):
        """Test successful POST request."""
        responses.add(
            responses.POST,
            "https://api.thecompaniesapi.com/v2/companies/search",
            json={"data": {"companies": []}},
            status=200
        )
        
        client = HttpClient(api_token="test-token")
        payload = {"query": [{"attribute": "name", "value": "test"}]}
        result = client.post("/v2/companies/search", json_data=payload)
        
        assert result == {"data": {"companies": []}}
        
        # Verify the request body
        request_body = json.loads(responses.calls[0].request.body)
        assert request_body == payload
    
    @responses.activate
    def test_request_error_handling(self):
        """Test error handling for HTTP errors."""
        responses.add(
            responses.GET,
            "https://api.thecompaniesapi.com/v2/error",
            status=404
        )
        
        client = HttpClient(api_token="test-token")
        
        with pytest.raises(ApiError, match="Request failed"):
            client.get("/v2/error")
    
    @responses.activate
    def test_non_json_response(self):
        """Test handling of non-JSON responses."""
        responses.add(
            responses.GET,
            "https://api.thecompaniesapi.com/v2/text",
            body="Plain text response",
            status=200
        )
        
        client = HttpClient(api_token="test-token")
        result = client.get("/v2/text")
        
        assert result == {"data": "Plain text response", "status": 200}


@pytest.mark.unit
class TestClient:
    """Test the main Client class."""
    
    def test_init_success(self):
        """Test successful client initialization."""
        client = Client(api_token="test-token")
        
        assert client.http.api_token == "test-token"
        assert isinstance(client.http, HttpClient)
    
    def test_init_no_token_error(self):
        """Test that Client raises error when no API token provided."""
        with pytest.raises(ValueError, match="api_token is required"):
            Client()
    
    def test_init_with_custom_params(self):
        """Test Client initialization with custom parameters."""
        client = Client(
            api_token="test-token",
            api_url="https://custom.api.com",
            visitor_id="visitor-123",
            timeout=60
        )
        
        assert client.http.api_token == "test-token"
        assert client.http.api_url == "https://custom.api.com"
        assert client.http.visitor_id == "visitor-123"
        assert client.http.timeout == 60
    
    @responses.activate
    def test_fetchApiHealth(self):
        """Test the dynamically generated fetchApiHealth method."""
        responses.add(
            responses.GET,
            "https://api.thecompaniesapi.com/",
            json={"status": "healthy"},
            status=200
        )
        
        client = Client(api_token="test-token")
        result = client.fetchApiHealth()
        
        assert result == {"status": "healthy"}
    
    def test_http_client_delegation(self):
        """Test that Client properly delegates to HttpClient."""
        client = Client(api_token="test-token")
        
        # Mock the HttpClient's get method
        with patch.object(client.http, 'get', return_value={"mocked": True}) as mock_get:
            result = client.fetchApiHealth()
            
            mock_get.assert_called_once_with('/', params={})
            assert result == {"mocked": True}
    
    def test_dynamic_operations_loading(self):
        """Test that operations are loaded dynamically from the generated schema."""
        client = Client(api_token="test-token")
        
        # Should have loaded operations from generated schema
        assert len(client._operations_map) > 0
        assert "fetchApiHealth" in client._operations_map
        
        # Test dynamic attribute access
        assert hasattr(client, "fetchApiHealth")
        
        # Test that non-existent methods raise AttributeError
        with pytest.raises(AttributeError):
            client.non_existent_method


@pytest.mark.unit
class TestApiError:
    """Test the ApiError exception class."""
    
    def test_api_error_creation(self):
        """Test ApiError can be created and raised."""
        error = ApiError("Test error message")
        assert str(error) == "Test error message"
        
        with pytest.raises(ApiError, match="Test error message"):
            raise error 
