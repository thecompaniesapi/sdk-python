# The Companies API SDK for Python

[![PyPI version][pypi-version-src]][pypi-version-href]
[![PyPI downloads][pypi-downloads-src]][pypi-downloads-href]
[![Python Support][python-src]][python-href]
[![License][license-src]][license-href]

A fully-featured Python SDK for [The Companies API](https://www.thecompaniesapi.com), providing type-safe access to company data, locations, industries, technologies, job titles, lists, and more.

If you need more details about a specific endpoint, you can find the corresponding documentation in [the API reference](https://www.thecompaniesapi.com/api).

You can also contact us on our [livechat](https://www.thecompaniesapi.com/) if you have any questions.

## 🚀 Features

- Expose all our 30+ endpoints and gives access to 50M+ companies from your codebase
- Type-safe API client with full access to our [OpenAPI](https://api.thecompaniesapi.com/v2/openapi) schemas
- Real-time company enrichment with both synchronous and asynchronous options
- Powerful search capabilities with filters, sorting and pagination
- Create and manage your company lists
- Track and monitor enrichment actions and requests
- Generate detailed analytics and insights for searches and lists
- Natural language querying for structured company information
- Lightweight with minimal dependencies

## 📦 Installation

```bash
pip install thecompaniesapi
```

**That's it!** The SDK includes pre-generated types and works immediately after installation.

## 🔑 Initialize the client

Get your API token from [your settings page](https://www.thecompaniesapi.com/settings/api-tokens) and initialize our client with `Client`.

The API token is required to authenticate your requests and should be kept secure. Never commit your API token to version control or share it publicly.

```python
from thecompaniesapi import Client

tca = Client(api_token='your-api-token')
```

## 🏬 Companies

### Search companies

📖 [Documentation](https://www.thecompaniesapi.com/api/search-companies)

🕹️ [Use case: How to build a company search engine with our API](https://www.thecompaniesapi.com/use-cases/companies-search-engine)

🔍 To learn more about our query system, please read our [documentation](https://www.thecompaniesapi.com/use-cases/companies-search-engine).

```python
# Search companies by industry and size
response = tca.search_companies(
    query=[
        {"attribute": "about.industries", "operator": "or", "sign": "equals", "values": ["computer-software"]},
        {"attribute": "about.totalEmployees", "operator": "or", "sign": "equals", "values": ["10-50"]}
    ],
    size=25
)

companies = response["data"]["companies"]  # Companies that match the query
meta = response["data"]["meta"]  # Meta information
```

### Search companies by name

📖 [Documentation](https://www.thecompaniesapi.com/api/search-companies-name)

🕹️ [Use case: Add a company search with autocomplete to your application](https://www.thecompaniesapi.com/use-cases/company-autocomplete)

```python
response = tca.search_companies_by_name(
    name="The Companies API",
    size=2
)

companies = response["data"]["companies"]  # Companies that match the name
meta = response["data"]["meta"]  # Meta information
```

### Search companies using a prompt

📖 [Documentation](https://www.thecompaniesapi.com/api/search-companies-prompt)

```python
# Search 25 companies for a specific prompt
response = tca.search_companies_by_prompt(
    prompt="SaaS Companies in the United States with more than 100 employees",
    size=25
)

companies = response["data"]["companies"]  # Companies that match the prompt
meta = response["data"]["meta"]  # Meta information
```

### Search similar companies

📖 [Documentation](https://www.thecompaniesapi.com/api/search-similar-companies)

```python
# Search 25 companies that are similar to Crisp and Intercom
response = tca.search_similar_companies(
    domains=["crisp.chat", "intercom.com"],
    size=25
)

companies = response["data"]["companies"]  # Companies that are similar to the domains
meta = response["data"]["meta"]  # Meta information
```

### Count companies matching your query

📖 [Documentation](https://www.thecompaniesapi.com/api/count-companies)

```python
# Count how many companies are in the computer-software industry
response = tca.count_companies(
    query=[
        {
            "attribute": "about.industries",
            "operator": "or",
            "sign": "equals",
            "values": ["computer-software"]
        }
    ]
)

count = response["data"]  # Number of companies that match the query
```

### Enrich a company from a domain name

📖 [Documentation](https://www.thecompaniesapi.com/api/enrich-company-from-domain)

```python
# Fetch company data from our database without enrichment (faster response)
response = tca.fetch_company(domain="microsoft.com")

company = response["data"]  # The company profile

# Fetch company data and re-analyze it in real-time to get fresh, up-to-date information (slower but more accurate)
response = tca.fetch_company(
    domain="microsoft.com",
    refresh=True
)

company = response["data"]  # The company profile
```

### Enrich a company from an email

📖 [Documentation](https://www.thecompaniesapi.com/api/enrich-company-from-email)

🕹️ [Use case: Enrich your users at signup with the latest information about their company](https://www.thecompaniesapi.com/use-cases/enrich-users-signup)

```python
# Fetch the company profile behind a professional email address
response = tca.fetch_company_by_email(email="jack@openai.com")

company = response["data"]  # The company profile
```

### Enrich a company from a social network URL

📖 [Documentation](https://www.thecompaniesapi.com/api/enrich-company-from-social-network-url)

```python
# Fetch the company profile behind a social network URL
response = tca.fetch_company_by_social(
    linkedin="https://www.linkedin.com/company/apple"
)

company = response["data"]  # The company profile
```

### Find a company email patterns

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-company-email-patterns)

```python
# Fetch the company email patterns for a specific domain
response = tca.fetch_company_email_patterns(domain="apple.com")

patterns = response["data"]  # The company email patterns
```

### Ask a question about a company

📖 [Documentation](https://www.thecompaniesapi.com/api/ask-company)

```python
# Ask what products a company offers using its domain
response = tca.ask_company(
    domain="microsoft.com",
    question="What products does this company offer?",
    model="large",  # 'small' is also available
    fields=[
        {
            "key": "products",
            "type": "array|string",
            "description": "The products that the company offers"
        }
    ]
)

answer = response["data"]["answer"]  # Structured AI response
meta = response["data"]["meta"]  # Meta information
```

### Fetch the context of a company

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-company-context)

```python
# Get AI-generated strategic insights about a company
response = tca.fetch_company_context(domain="microsoft.com")

context = response["data"]["context"]  # Includes market, model, differentiators, etc.
meta = response["data"]["meta"]  # Meta information
```

### Fetch analytics data for a query or your lists

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-companies-analytics)

```python
# Analyze company distribution by business type
response = tca.fetch_companies_analytics(
    attribute="about.businessType",
    query=[
        {
            "attribute": "locations.headquarters.country.code",
            "operator": "or",
            "sign": "equals",
            "values": ["us", "gb", "fr"]
        }
    ]
)

analytics = response["data"]["data"]  # Aggregated values
meta = response["data"]["meta"]  # Meta information
```

### Export analytics data in multiple formats for a search

📖 [Documentation](https://www.thecompaniesapi.com/api/export-companies-analytics)

```python
# Export analytics to CSV
response = tca.export_companies_analytics(
    format="csv",
    attributes=["about.industries", "about.totalEmployees"],
    query=[
        {
            "attribute": "technologies.active",
            "operator": "or",
            "sign": "equals",
            "values": ["shopify"]
        }
    ]
)

analytics = response["data"]["data"]  # Aggregated values
meta = response["data"]["meta"]  # Meta information
```

## 🎯 Actions

### Request an action on one or more companies

📖 [Documentation](https://www.thecompaniesapi.com/api/request-action)

```python
# Request an enrichment job on multiple companies
response = tca.request_action(
    domains=["microsoft.com", "apple.com"],
    job="enrich-companies",
    estimate=False
)

actions = response["data"]["actions"]  # Track this via fetch_actions
meta = response["data"]["meta"]  # Meta information
```

### Fetch the actions for your actions

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-actions)

```python
# Fetch recent actions
response = tca.fetch_actions(
    status="completed",
    page=1,
    size=5
)

actions = response["data"]["actions"]  # Actions that match the query
meta = response["data"]["meta"]  # Meta information
```

## 🏭 Industries

### Search industries

📖 [Documentation](https://www.thecompaniesapi.com/api/search-industries)

```python
# Search industries by keyword
response = tca.search_industries(
    search="software",
    size=10
)

industries = response["data"]["industries"]  # Industries that match the keyword
meta = response["data"]["meta"]  # Meta information
```

### Find similar industries

📖 [Documentation](https://www.thecompaniesapi.com/api/find-similar-industries)

```python
# Find industries similar to given ones
response = tca.search_industries_similar(
    industries=["saas", "fintech"]
)

similar = response["data"]["industries"]  # Industries that are similar to the given ones
meta = response["data"]["meta"]  # Meta information
```

## ⚛️ Technologies

### Search technologies

📖 [Documentation](https://www.thecompaniesapi.com/api/search-technologies)

```python
# Search technologies by keyword
response = tca.search_technologies(
    search="shopify",
    size=10
)

technologies = response["data"]["technologies"]  # Technologies that match the keyword
meta = response["data"]["meta"]  # Meta information
```

## 🌍 Locations

### Search cities

📖 [Documentation](https://www.thecompaniesapi.com/api/search-cities)

```python
# Search cities by name
response = tca.search_cities(
    search="new york",
    size=5
)

cities = response["data"]["cities"]  # Cities that match the name
meta = response["data"]["meta"]  # Meta information
```

### Search counties

📖 [Documentation](https://www.thecompaniesapi.com/api/search-counties)

```python
# Search counties by name
response = tca.search_counties(
    search="orange",
    size=5
)

counties = response["data"]["counties"]  # Counties that match the name
meta = response["data"]["meta"]  # Meta information
```

### Search states

📖 [Documentation](https://www.thecompaniesapi.com/api/search-states)

```python
# Search states by name
response = tca.search_states(
    search="california",
    size=5
)

states = response["data"]["states"]  # States that match the name
meta = response["data"]["meta"]  # Meta information
```

### Search countries

📖 [Documentation](https://www.thecompaniesapi.com/api/search-countries)

```python
# Search countries by name
response = tca.search_countries(
    search="france",
    size=5
)

countries = response["data"]["countries"]  # Countries that match the name
meta = response["data"]["meta"]  # Meta information
```

### Search continents

📖 [Documentation](https://www.thecompaniesapi.com/api/search-continents)

```python
# Search continents by name
response = tca.search_continents(
    search="asia",
    size=5
)

continents = response["data"]["continents"]  # Continents that match the name
meta = response["data"]["meta"]  # Meta information
```

## 💼 Job titles

### Enrich a job title from its name

📖 [Documentation](https://www.thecompaniesapi.com/api/enrich-job-title-from-name)

```python
# Enrich "chief marketing officer"
response = tca.enrich_job_titles(name="chief marketing officer")

job_title = response["data"]  # Contains department, seniority, etc.
```

## 📋 Lists

### Fetch your lists

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-lists)

```python
# Fetch your lists
response = tca.fetch_lists()

lists = response["data"]["lists"]  # Lists that match the query
meta = response["data"]["meta"]  # Meta information
```

### Create a list of companies

📖 [Documentation](https://www.thecompaniesapi.com/api/create-list)

```python
# Create a list of companies
response = tca.create_list(
    name="My SaaS List",
    type="companies"
)

new_list = response["data"]  # The new list
```

### Fetch companies in your list

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-companies-in-list)

```python
# Fetch companies in a list
response = tca.fetch_companies_in_list(list_id=1234)

companies = response["data"]["companies"]  # Companies that match the list
meta = response["data"]["meta"]  # Meta information
```

### Add or remove companies in your list

📖 [Documentation](https://www.thecompaniesapi.com/api/toggle-companies-in-list)

```python
# Add companies to a list
response = tca.toggle_companies_in_list(
    list_id=1234,
    companies=["apple.com", "stripe.com"]
)

list_data = response["data"]  # The updated list
```

## 👥 Teams

### Fetch your team

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-team)

```python
# Fetch your team details
response = tca.fetch_team()

team = response["data"]  # Your team details
```

## 🔧 Utilities

### Fetch the health of the API

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-api-health)

```python
# Check API health status
response = tca.fetch_api_health()

health = response["data"]  # The health of the API
```

### Fetch the OpenAPI schema

📖 [Documentation](https://www.thecompaniesapi.com/api/fetch-openapi)

```python
# Fetch OpenAPI schema
response = tca.fetch_openapi()

schema = response["data"]  # The OpenAPI schema
```

## 🧪 Testing

### Unit Tests

Run the unit tests that don't require an API token:

```bash
pytest tests/test_client.py -m unit
```

### Integration Tests

The SDK includes comprehensive integration tests that make real API calls. To run them:

1. **Create a `.env` file** in the project root:
   ```bash
   # Required: Your API token from https://www.thecompaniesapi.com/settings/api-tokens
   TCA_API_TOKEN=your-api-token-here
   
   # Optional configurations
   TCA_API_URL=https://api.thecompaniesapi.com
   TCA_VISITOR_ID=your-visitor-id
   TCA_TIMEOUT=30
   ```

2. **Install test dependencies:**
   ```bash
   pip install -e ".[test]"
   ```

3. **Run integration tests:**
   ```bash
   # Run all integration tests
   pytest tests/test_integration.py -m integration -v
   
   # Run all tests except integration tests
   pytest -m "not integration"
   
   # Run all tests (unit + integration)
   pytest
   ```

The integration tests cover:
- Company search (GET and POST methods)
- Company counting and filtering
- Company lookup by email and domain
- Complex query serialization
- Error handling and edge cases
- Dynamic method access
- API health checks

## 🔗 Links

- [The Companies API](https://www.thecompaniesapi.com)
- [API Documentation](https://www.thecompaniesapi.com/api)
- [TypeScript SDK](https://github.com/thecompaniesapi/sdk-typescript)
- [Support & Live Chat](https://www.thecompaniesapi.com/)

## 📄 License

[MIT](./LICENSE) License © [TheCompaniesAPI](https://github.com/thecompaniesapi)

[pypi-version-src]: https://img.shields.io/pypi/v/thecompaniesapi?style=flat&colorA=080f12&colorB=1fa669
[pypi-version-href]: https://pypi.org/project/thecompaniesapi/
[pypi-downloads-src]: https://img.shields.io/pypi/dm/thecompaniesapi?style=flat&colorA=080f12&colorB=1fa669
[pypi-downloads-href]: https://pypi.org/project/thecompaniesapi/
[python-src]: https://img.shields.io/pypi/pyversions/thecompaniesapi?style=flat&colorA=080f12&colorB=1fa669
[python-href]: https://pypi.org/project/thecompaniesapi/
[license-src]: https://img.shields.io/github/license/thecompaniesapi/sdk-python.svg?style=flat&colorA=080f12&colorB=1fa669
[license-href]: https://github.com/thecompaniesapi/sdk-python/blob/main/LICENSE
