# Testing the Weather Data Platform Backend

This document describes the testing approach and infrastructure for the Weather Data Platform's backend.

## Test Coverage

The backend has a comprehensive test suite with 98% code coverage as of September 12, 2025. This ensures that the application is robust and behaves as expected under various conditions.

### Coverage Report

```
Name                                        Stmts   Miss  Cover
---------------------------------------------------------------
weather/__init__.py                             0      0   100%
weather/admin.py                                8      0   100%
weather/apps.py                                 4      0   100%
weather/integration/__init__.py                 0      0   100%
weather/integration/clients/__init__.py         0      0   100%
weather/integration/clients/geocoding.py       32      2    94%
weather/integration/clients/weather.py         20      2    90%
weather/integration/services/__init__.py        0      0   100%
weather/integration/services/geocoding.py       7      0   100%
weather/integration/services/weather.py        69      8    88%
weather/migrations/0001_initial.py              5      0   100%
weather/migrations/__init__.py                  0      0   100%
weather/models.py                              11      0   100%
weather/serializers.py                         17      0   100%
weather/urls.py                                 3      0   100%
weather/utils/__init__.py                       0      0   100%
weather/utils/cache_utils.py                    5      0   100%
weather/utils/constants.py                      9      0   100%
weather/utils/date_utils.py                     5      0   100%
weather/utils/error_handlers.py                15      0   100%
weather/views.py                               44      0   100%
---------------------------------------------------------------
TOTAL                                         642     13    98%
```

## Test Structure

The tests are organized in a modular structure under the `weather/tests/` directory:

- `test_models.py`: Tests for the WeatherData model
- `test_views.py`: Tests for the API views
- `test_weather_service.py`: Tests for the WeatherService
- `test_geocoding_service.py`: Tests for the GeocodingService
- `test_utils.py`: Tests for utility functions (date_utils, cache_utils, error_handlers)
- `test_weather_client.py`: Tests for the WeatherClient
- `contract/`: Contract tests for external API integrations

## Running Tests

Tests are run using pytest. The project is configured with pytest-django to handle Django-specific testing needs and pytest-cov for coverage reports.

### Running All Tests

To run all tests:

```bash
# On Linux/macOS
./dev.sh test-backend

# On Windows PowerShell
.\dev.ps1 test-backend
```

Alternatively, you can run the tests directly in the backend container:

```bash
# Run all tests
docker-compose exec backend pytest

# Run tests with coverage report
docker-compose exec backend pytest --cov=weather
```

### Running Specific Tests

To run specific test files or classes:

```bash
# Run a specific test file
docker-compose exec backend pytest weather/tests/test_views.py

# Run a specific test class
docker-compose exec backend pytest weather/tests/test_views.py::TestWeatherAverageView

# Run a specific test method
docker-compose exec backend pytest weather/tests/test_views.py::TestWeatherAverageView::test_successful_response
```

### Running Contract Tests

Contract tests make actual API calls to external services. They should be run separately from regular unit tests:

```bash
# Run only contract tests
docker-compose exec backend pytest -m contract

# Run contract tests for a specific API
docker-compose exec backend pytest weather/tests/contract/test_weather_api_contract.py
```

These tests verify that our expectations of external API responses match reality. They should be run:
- After external APIs announce changes
- Periodically (e.g., monthly) to detect unannounced changes
- Before major releases to ensure compatibility

Contract tests store the API response schema and a sample response in the `weather/tests/contract/contracts/` directory. When API responses change, these tests help identify exactly what changed.

## Test Configuration

The testing configuration is in `backend/pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = weatherapi.settings
python_files = tests.py test_*.py *_tests.py
markers =
    contract: marks tests as contract tests (run separately, makes real API calls)
```

## Mocking External Services

The tests use Python's `unittest.mock` to mock external services like the weather and geocoding APIs. This ensures that tests can run without making actual network requests and provides consistent test results.

## Contract Testing

Contract testing is our approach to validate that our assumptions about external API responses remain valid over time. 

Each contract test:
1. Makes a real API call to the external service
2. Validates the response against our expected schema
3. Stores the response for future reference
4. Reports detailed information about any schema changes

If an API changes, the contract tests identify exactly what changed, making it easier to update our code.

## Integration with CI/CD

The regular unit tests are automatically run as part of the CI/CD pipeline. A build will fail if any tests fail or if the coverage drops below a certain threshold.

Contract tests are not run in the regular CI/CD pipeline due to their dependence on external services. Instead, they are run:
- On a scheduled basis (e.g., weekly)
- Manually before major releases
- When investigating integration issues

## Future Test Improvements

Areas for future test enhancement:

1. Add more integration tests that test the full request/response cycle
2. Add performance tests for critical endpoints
3. Expand contract testing to cover more edge cases
4. Add load testing for high-traffic scenarios