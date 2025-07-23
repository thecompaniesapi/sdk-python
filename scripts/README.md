# Scripts

This directory contains utility scripts for maintaining the SDK.

## Schema Generation

### `generate_schema.py`

Fetches the OpenAPI schema from The Companies API and generates Python types and operations map.

> **Note**: Generated code is **included in the pip package**, so end users don't need to run this script. This is only for SDK maintainers when the API schema changes.

#### Usage (For SDK Maintainers)

```bash
# Install code generation dependencies
pip install -e ".[codegen]"

# Run the generation script
python scripts/generate_schema.py

# Commit the updated generated files
git add src/thecompaniesapi/generated/
git commit -m "Update generated schema"
```

#### Environment Variables

- `TCA_API_VERSION` - API version to use (default: `v2`)
- `TCA_API_URL` - Base API URL (default: `https://api.thecompaniesapi.com`)

#### Generated Files

The script generates the following files in `src/thecompaniesapi/generated/`:

- `models.py` - Pydantic models for all API types
- `operations_map.py` - Operations map with paths, methods, and parameters
- `__init__.py` - Exports for the generated module

#### Example

```bash
# Generate with custom API version
TCA_API_VERSION=v2 python scripts/generate_schema.py

# Generate from staging environment
TCA_API_URL=https://staging-api.thecompaniesapi.com python scripts/generate_schema.py
```

The generated types are automatically picked up by the `Client` class to provide type-safe method calls.

#### When to Regenerate

Regenerate and commit the files when:
- The Companies API OpenAPI schema is updated
- New endpoints are added  
- Existing endpoint signatures change
- Response models are modified

#### For End Users

End users of the pip package (`pip install thecompaniesapi`) get pre-generated code and don't need to run any generation scripts. The SDK works out of the box. 
