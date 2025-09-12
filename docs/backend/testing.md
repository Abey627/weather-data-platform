# Testing the Weather Data Platform Backend

This document describes the testing approach and infrastructure for the Weather Data Platform's backend.

## Overview

Our testing approach is guided by a few key principles:

- **High Coverage**: We maintain 95%+ test coverage (currently at 98%)
- **Isolation**: Tests don't depend on external services or state
- **Speed**: Test suite runs quickly to encourage frequent testing
- **Readability**: Tests serve as documentation
- **Maintainability**: Tests are easy to update when requirements change

## Quick Setup Guide

### 1. Running Tests

```bash
# Using dev scripts (recommended)
.\dev.ps1 test-backend    # Windows
./dev.sh test-backend     # Linux/macOS

# Directly with Docker
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=weather  # With coverage

# Running specific tests
docker-compose exec backend pytest weather/tests/test_views.py
docker-compose exec backend pytest weather/tests/test_views.py::TestWeatherAverageView
docker-compose exec backend pytest -m contract  # Only contract tests
```

### 2. Test Configuration

Our pytest configuration is in `backend/pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = weatherapi.settings
python_files = tests.py test_*.py *_tests.py
markers =
    contract: marks tests as contract tests (run separately, makes real API calls)
```

### 3. Test Structure

Tests are organized in `weather/tests/`:

- `test_models.py` - Tests for the WeatherData model
- `test_views.py` - Tests for API views
- `test_weather_service.py` - Tests for WeatherService
- `test_geocoding_service.py` - Tests for GeocodingService
- `test_utils.py` - Tests for utility functions
- `test_weather_client.py` - Tests for WeatherClient
- `contract/` - Contract tests for external API integrations

#### Test Organization Guidelines

To maintain consistency across our test suite:

1. **File Organization**: Each test file should focus on testing a specific component type:
   - Model tests go in `test_models.py`
   - View/API endpoint tests go in `test_views.py`
   - Client tests go in `test_*_client.py`
   - Service tests go in `test_*_service.py`

2. **Naming Conventions**:
   - Prefer pytest-style class names: `TestClassName` (not `ClassNameTests`)
   - Test method names should clearly describe what they're testing
   - Use docstrings to provide additional context

## Writing Tests

### Key Pytest Features We Use

- **Fixtures**: Reusable test components (see examples in `test_views.py`)
- **Parametrization**: Test multiple scenarios with a single function
- **Markers**: Categorize tests (e.g., `@pytest.mark.contract`)
- **Class organization**: Group related tests within a class
- **pytest-django**: Django-specific testing utilities
- **pytest-cov**: Coverage reporting

### Testing Framework Standards

We use pytest as our primary testing framework with the following guidelines:

1. **Framework Preference**: 
   - Use pytest for all new tests
   - Prefer pytest fixtures over setUp/tearDown methods
   - Use pytest.mark decorators for test categorization

2. **Mocking Approach**:
   - Use `unittest.mock.patch` consistently for mocking
   - Prefer fixture-based mocks when possible
   - Document complex mocking setups with comments

3. **Test Independence**:
   - Each test should be independent and not rely on the state from other tests
   - Use fixtures to set up and tear down test data
   - Reset any global state between tests

### Test Patterns by Component

| Component | What to Test |
|-----------|--------------|
| **Models** | Validation logic, model methods, default values |
| **Views** | Response codes, valid/invalid inputs, auth checks |
| **Services/Clients** | Error handling, retry logic, edge cases |
| **Utilities** | Edge cases, input variations |

### Mocking External Services

Use `unittest.mock` to isolate tests from external dependencies:

```python
@patch('weather.integration.clients.weather.requests.get')
def test_weather_client(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'example': 'data'}
    mock_get.return_value = mock_response
    
    # Test code here
```

## Contract Testing

Contract tests validate our assumptions about external API responses:

1. They make real API calls to external services
2. Validate responses against expected schemas
3. Should be run:
   - After external APIs announce changes
   - Periodically (monthly) to detect unannounced changes
   - Before major releases

```bash
# Run contract tests
docker-compose exec backend pytest -m contract
```

Contract tests store API response schemas and sample responses in the `weather/tests/contract/contracts/` directory. When API responses change, these tests help identify exactly what changed.

## CI/CD Integration

- Regular tests run on every build
- Builds fail if tests fail or coverage drops below threshold
- Contract tests run:
  - On a scheduled basis (weekly)
  - Manually before releases
  - When investigating integration issues

## Future Improvements

1. Add more integration tests for the full request/response cycle
2. Add performance tests for critical endpoints
3. Expand contract testing to cover more edge cases
4. Add load testing for high-traffic scenarios
5. Standardize remaining tests to use pytest consistently
6. Refactor Django TestCase-based tests to use pytest fixtures