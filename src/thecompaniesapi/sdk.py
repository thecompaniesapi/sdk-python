import json
import urllib.parse
from typing import Any, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class HttpClient:
    """
    Base HTTP client for The Companies API.
    Handles authentication, request serialization, and response handling.
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        api_url: str = "https://api.thecompaniesapi.com",
        visitor_id: Optional[str] = None,
        timeout: int = 300
    ):
        self.api_token = api_token
        self.api_url = api_url.rstrip('/')
        self.visitor_id = visitor_id
        self.timeout = timeout
        
        # Create session with retry strategy
        self.session = requests.Session()
        
        # Configure retry strategy
        retry_strategy = Retry(
            total=3,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE"],
            backoff_factor=1
        )
        
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Set default headers
        self._setup_default_headers()
    
    def _setup_default_headers(self) -> None:
        """Setup default headers for all requests."""
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'User-Agent': 'thecompaniesapi-python-sdk/0.0.1'
        })
        
        # Add authorization if token provided
        if self.api_token:
            self.session.headers['Authorization'] = f'Basic {self.api_token}'
        
        # Add visitor ID if provided
        if self.visitor_id:
            self.session.headers['Tca-Visitor-Id'] = self.visitor_id
    
    def _serialize_query_params(self, params: Dict[str, Any]) -> Dict[str, str]:
        """
        Serialize query parameters, converting objects and arrays to JSON strings.
        """
        serialized = {}
        
        for key, value in params.items():
            if value is None:
                continue
            elif isinstance(value, (dict, list)):
                # Convert objects and arrays to JSON strings and URL encode them
                # This matches: encodeURIComponent(JSON.stringify(query[key]))
                json_str = json.dumps(value, separators=(',', ':'))  # Compact JSON
                serialized[key] = urllib.parse.quote(json_str)
            elif isinstance(value, bool):
                # Convert boolean to lowercase string  
                serialized[key] = str(value).lower()
            else:
                # Convert everything else to string
                serialized[key] = str(value)
        
        return serialized
    
    def _prepare_url(self, path: str) -> str:
        """Prepare the full URL for a request."""
        # Ensure path starts with /
        if not path.startswith('/'):
            path = f'/{path}'
        
        return f'{self.api_url}{path}'
    
    def _make_request(
        self,
        method: str,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request with proper error handling and response parsing.
        """
        url = self._prepare_url(path)
        
        # Prepare query parameters
        query_params = None
        if params:
            query_params = self._serialize_query_params(params)
        
        # Prepare request headers
        request_headers = {}
        if headers:
            request_headers.update(headers)
        
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                params=query_params,
                json=json_data,
                headers=request_headers,
                timeout=self.timeout
            )
            
            # Raise an exception for bad status codes
            response.raise_for_status()
            
            # Try to parse JSON response
            try:
                return response.json()
            except json.JSONDecodeError:
                # If response is not JSON, return text content
                return {'data': response.text, 'status': response.status_code}
                
        except requests.exceptions.RequestException as e:
            # Handle request errors
            raise ApiError(f"Request failed: {str(e)}") from e
    
    def get(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a GET request."""
        return self._make_request('GET', path, params=params, headers=headers)
    
    def post(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a POST request."""
        return self._make_request('POST', path, params=params, json_data=json_data, headers=headers)
    
    def put(
        self,
        path: str,
        json_data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a PUT request."""
        return self._make_request('PUT', path, params=params, json_data=json_data, headers=headers)
    
    def delete(
        self,
        path: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make a DELETE request."""
        return self._make_request('DELETE', path, params=params, headers=headers)


class ApiError(Exception):
    """Custom exception for API errors."""
    pass


class Client:
    """
    Main client for The Companies API.
    This will be extended with operation methods generated from the OpenAPI schema.
    """
    
    def __init__(
        self,
        api_token: Optional[str] = None,
        api_url: str = "https://api.thecompaniesapi.com",
        visitor_id: Optional[str] = None,
        timeout: int = 300
    ):
        if not api_token:
            raise ValueError("api_token is required")
        
        self.http = HttpClient(
            api_token=api_token,
            api_url=api_url,
            visitor_id=visitor_id,
            timeout=timeout
        )
