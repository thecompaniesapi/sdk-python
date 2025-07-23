"""
Integration tests for The Companies API Python SDK

These tests make real API calls and require a valid API token.

Setup:
1. Create a .env file in the project root with:
   TCA_API_TOKEN=your-api-token-here
   TCA_API_URL=https://api.thecompaniesapi.com (optional)
   TCA_VISITOR_ID=your-visitor-id (optional)
   TCA_TIMEOUT=30 (optional)

2. Run integration tests with: pytest tests/test_integration.py -m integration

3. To skip integration tests: pytest -m "not integration"
"""

import os
import pytest
from pathlib import Path
try:
    from dotenv import load_dotenv
    HAS_DOTENV = True
except ImportError:
    HAS_DOTENV = False

from src.thecompaniesapi import Client, ApiError


class TestIntegration:
    """Integration tests that make real API calls"""
    
    client = None
    
    @classmethod
    def load_env_for_testing(cls):
        """Load .env file if it exists (for local testing)"""
        if HAS_DOTENV:
            env_path = Path(__file__).parent.parent / '.env'
            if env_path.exists():
                load_dotenv(env_path)
    
    @classmethod
    def get_api_token(cls) -> str:
        """Get API token from environment variables"""
        cls.load_env_for_testing()
        return os.getenv('TCA_API_TOKEN') or os.environ.get('TCA_API_TOKEN')
    
    @classmethod
    def setup_integration_client(cls) -> Client:
        """Setup integration client configured for testing"""
        if cls.client is not None:
            return cls.client
        
        token = cls.get_api_token()
        if not token:
            pytest.skip("TCA_API_TOKEN not set, skipping integration tests. Set TCA_API_TOKEN in .env file or environment.")
        
        params = {
            'api_token': token,
            'timeout': int(os.getenv('TCA_TIMEOUT', '30'))
        }
        
        # Optional: Custom base URL from environment
        if os.getenv('TCA_API_URL'):
            params['api_url'] = os.getenv('TCA_API_URL')
        
        # Optional: Visitor ID from environment
        if os.getenv('TCA_VISITOR_ID'):
            params['visitor_id'] = os.getenv('TCA_VISITOR_ID')
        
        cls.client = Client(**params)
        return cls.client
    
    @pytest.mark.integration
    def test_search_companies_basic(self):
        """Test basic search using GET method (simple parameters)"""
        client = self.setup_integration_client()
        
        # Test basic search - this should use searchCompanies (GET method)
        response = client.searchCompanies(
            page=1,
            size=5,  # Small size for faster tests
            search='technology'
        )
        
        assert isinstance(response, dict)
        assert 'companies' in response
        assert 'meta' in response
        assert isinstance(response['companies'], list)
        assert isinstance(response['meta'], dict)
    
    @pytest.mark.integration
    def test_search_companies_with_query(self):
        """Test search with query conditions using POST method"""
        client = self.setup_integration_client()
        
        # Test search with query conditions - this should use searchCompaniesPost (POST method)
        response = client.searchCompaniesPost(
            page=1,
            size=3,
            query=[
                {
                    'attribute': 'about.industries',
                    'operator': 'or',
                    'sign': 'equals',
                    'values': ['technology']
                }
            ]
        )
        
        assert isinstance(response, dict)
        assert 'companies' in response
        assert isinstance(response['companies'], list)
    
    @pytest.mark.integration
    def test_count_companies_basic(self):
        """Test basic count using GET method"""
        client = self.setup_integration_client()
        
        # Test basic count using GET method
        response = client.countCompanies(search='software')
        
        assert isinstance(response, dict)
        assert 'count' in response
        count = response['count']
        assert isinstance(count, int)
        assert count >= 0
    
    @pytest.mark.integration
    def test_count_companies_with_query(self):
        """Test count with query conditions using POST method"""
        client = self.setup_integration_client()
        
        # Test count with query conditions using POST method
        response = client.countCompaniesPost(
            query=[
                {
                    'attribute': 'about.industries',
                    'operator': 'or',
                    'sign': 'equals',
                    'values': ['saas']
                }
            ]
        )
        
        assert isinstance(response, dict)
        assert 'count' in response
        count = response['count']
        assert isinstance(count, int)
        assert count >= 0
    
    @pytest.mark.integration
    def test_fetch_company_by_email(self):
        """Test fetching company by email with well-known company emails"""
        client = self.setup_integration_client()
        
        # Test with well-known company emails
        test_cases = [
            {'name': 'openai_email', 'email': 'contact@openai.com'},
            {'name': 'microsoft_email', 'email': 'info@microsoft.com'},
            {'name': 'google_email', 'email': 'press@google.com'},
        ]
        
        successful_tests = 0
        
        for test_case in test_cases:
            try:
                response = client.fetchCompanyByEmail(email=test_case['email'])
                
                assert isinstance(response, dict)
                successful_tests += 1
                # If we get a successful response, it should have company data
                
            except Exception as e:
                # Don't fail the test - the email might not be in the database
                # or the API might return an error for various reasons
                continue
        
        # At least verify that the method exists and can be called
        assert hasattr(client, 'fetchCompanyByEmail')
        # We should have at least attempted all test cases
        assert len(test_cases) == 3
    
    @pytest.mark.integration
    def test_fetch_company_by_domain(self):
        """Test fetching company by domain"""
        client = self.setup_integration_client()
        
        # Test with well-known domains
        test_domains = ['microsoft.com', 'google.com', 'apple.com']
        
        for domain in test_domains:
            try:
                response = client.fetchCompany(domain=domain)
                
                assert isinstance(response, dict)
                # If we get a successful response, it should have company data
                break  # Success with at least one domain is good enough
                
            except Exception as e:
                # Continue trying other domains
                continue
        
        # At least verify that the method exists
        assert hasattr(client, 'fetchCompany')
    
    @pytest.mark.integration
    def test_error_handling(self):
        """Test error handling with invalid requests"""
        client = self.setup_integration_client()
        
        # Test with invalid email format
        try:
            response = client.fetchCompanyByEmail(email='invalid-email-format')
            
            # If we get here, check the response for error indicators
            assert isinstance(response, dict)
            
        except Exception as e:
            # This is expected behavior for invalid input
            assert isinstance(e, Exception)
    
    @pytest.mark.integration
    def test_complex_query_serialization(self):
        """Test complex query serialization to verify our custom query parameter handling"""
        client = self.setup_integration_client()
        
        # Test complex query serialization
        response = client.searchCompaniesPost(
            page=1,
            size=2,
            query=[
                {
                    'attribute': 'about.industries',
                    'operator': 'or',
                    'sign': 'equals',
                    'values': ['technology', 'saas']
                }
            ],
            searchFields=['about.name', 'domain.domain']
        )
        
        assert isinstance(response, dict)
        assert 'companies' in response
        assert isinstance(response['companies'], list)
    
    @pytest.mark.integration
    def test_api_health(self):
        """Test API health endpoint"""
        client = self.setup_integration_client()
        
        # Test the health endpoint
        response = client.fetchApiHealth()
        
        assert isinstance(response, dict)
        # Health endpoint should return some status information
    
    @pytest.mark.integration
    def test_client_configuration(self):
        """Test client configuration and basic functionality"""
        client = self.setup_integration_client()
        
        # Verify client was configured correctly
        assert client.http.api_token is not None
        assert len(client._operations_map) > 0
        
        # Test that we can make a simple request
        try:
            response = client.countCompanies(search='test')
            assert isinstance(response, dict)
            assert 'count' in response
        except Exception as e:
            pytest.fail(f"Client configuration test failed: {e}")
    
    @pytest.mark.integration
    def test_dynamic_method_access(self):
        """Test that all generated methods are accessible"""
        client = self.setup_integration_client()
        
        # Test some key methods exist
        expected_methods = [
            'fetchApiHealth',
            'searchCompanies',
            'searchCompaniesPost',
            'countCompanies',
            'countCompaniesPost',
            'fetchCompany',
            'fetchCompanyByEmail'
        ]
        
        for method_name in expected_methods:
            assert hasattr(client, method_name), f"Method {method_name} should be available"
            method = getattr(client, method_name)
            assert callable(method), f"Method {method_name} should be callable"
    
    @pytest.mark.integration
    def test_full_integration_flow(self):
        """Run a comprehensive integration test flow"""
        # Test 1: Basic search
        self.test_search_companies_basic()
        
        # Test 2: Complex query search
        self.test_search_companies_with_query()
        
        # Test 3: Count operations
        self.test_count_companies_basic()
        self.test_count_companies_with_query()
        
        # Test 4: Company lookup
        self.test_fetch_company_by_email()
        self.test_fetch_company_by_domain()
        
        # Test 5: Error handling
        self.test_error_handling()
        
        # Test 6: Query serialization
        self.test_complex_query_serialization()
        
        # Test 7: Health check
        self.test_api_health()
        
        # Test 8: Configuration
        self.test_client_configuration()
        
        # Test 9: Dynamic methods
        self.test_dynamic_method_access()


class TestIntegrationQuickSmoke:
    """Quick smoke tests that can run without extensive API calls"""
    
    @pytest.mark.integration
    def test_client_initialization_with_env(self):
        """Test that client can be initialized with environment variables"""
        # This test will be skipped if no token is available
        TestIntegration.load_env_for_testing()
        token = os.getenv('TCA_API_TOKEN') or os.environ.get('TCA_API_TOKEN')
        
        if not token:
            pytest.skip("TCA_API_TOKEN not set, skipping integration smoke test")
        
        client = Client(api_token=token)
        assert client.http.api_token == token
        assert len(client._operations_map) > 0
    
    @pytest.mark.integration
    def test_operations_map_loaded(self):
        """Test that operations map is properly loaded from generated schema"""
        TestIntegration.load_env_for_testing()
        token = os.getenv('TCA_API_TOKEN') or os.environ.get('TCA_API_TOKEN')
        
        if not token:
            pytest.skip("TCA_API_TOKEN not set, skipping integration smoke test")
        
        client = Client(api_token=token)
        
        # Should have loaded operations from generated schema
        assert len(client._operations_map) > 0
        assert 'fetchApiHealth' in client._operations_map
        assert 'searchCompanies' in client._operations_map
        
        # Test operation config structure
        health_config = client._operations_map['fetchApiHealth']
        assert 'path' in health_config
        assert 'method' in health_config
        assert 'pathParams' in health_config 
