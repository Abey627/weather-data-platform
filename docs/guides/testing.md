# Testing Guide

This document describes the testing approach, infrastructure, and procedures for the Weather Data Platform.

## Testing Overview

Our testing approach is guided by a few key principles:

- **High Coverage**: We maintain 95%+ test coverage (currently at 98% for the backend)
- **Isolation**: Tests don't depend on external services or state
- **Speed**: Test suite runs quickly to encourage frequent testing
- **Readability**: Tests serve as documentation
- **Maintainability**: Tests are easy to update when requirements change

## Backend Testing (✅ Implemented)

### Testing Stack

- **Framework**: pytest with pytest-django
- **Coverage**: pytest-cov
- **Mocking**: unittest.mock
- **Assertions**: pytest built-in assertions
- **Contract Testing**: Custom JSON schema validators

### Quick Setup Guide

#### Running Tests

```bash
# Using Docker Compose
docker-compose exec backend pytest
docker-compose exec backend pytest --cov=weather  # With coverage

# Running specific tests
docker-compose exec backend pytest weather/tests/test_views.py
docker-compose exec backend pytest weather/tests/test_views.py::TestWeatherAverageView
docker-compose exec backend pytest -m contract  # Only contract tests
```

#### Test Configuration

Our pytest configuration is in `backend/pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = weatherapi.settings
python_files = tests.py test_*.py *_tests.py
markers =
    contract: marks tests as contract tests (run separately, makes real API calls)
```

### Test Structure

Tests are organized in `weather/tests/`:

- `test_models.py` - Tests for the WeatherData model
- `test_views.py` - Tests for API views
- `test_weather_service.py` - Tests for WeatherService
- `test_geocoding_service.py` - Tests for GeocodingService
- `test_utils.py` - Tests for utility functions
- `test_weather_client.py` - Tests for WeatherClient
- `contract/` - Contract tests for external API integrations

### Test Organization Guidelines

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

### Key Pytest Features We Use

- **Fixtures**: Reusable test components (see examples in `test_views.py`)
- **Parametrization**: Test multiple scenarios with a single function
- **Markers**: Categorize tests (e.g., `@pytest.mark.contract`)
- **Class organization**: Group related tests within a class
- **pytest-django**: Django-specific testing utilities
- **pytest-cov**: Coverage reporting

### Framework Standards

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

### Contract Testing

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

## Frontend Testing (📝 Planned)

Once the frontend implementation begins, we plan to implement:

### Testing Stack (Planned)

- **Framework**: Jest
- **Component Testing**: React Testing Library
- **E2E Testing**: Cypress (potentially)

### Planned Test Types

1. **Unit Tests**: 
   - Testing utility functions
   - Testing hooks
   - Testing state management

2. **Component Tests**:
   - Testing individual UI components
   - Testing component rendering and interactions
   - Testing component props and state

3. **Integration Tests**:
   - Testing component interaction
   - Testing form submission flows
   - Testing API integration

### Frontend Test Structure (Planned)

Tests will be organized alongside the components:

```
frontend/
├── src/
│   ├── components/
│   │   ├── SearchForm/
│   │   │   ├── SearchForm.js
│   │   │   └── SearchForm.test.js  # Component test
│   │   └── ...
│   ├── utils/
│   │   ├── dateUtils.js
│   │   └── dateUtils.test.js       # Unit test
│   └── ...
└── cypress/                        # E2E tests (if implemented)
```

## Performance Testing (📝 Planned)

We plan to implement performance testing to ensure the API can handle expected load:

- **Load Testing**: Simulating multiple concurrent users
- **Stress Testing**: Testing the system beyond normal operational capacity
- **Endurance Testing**: Testing the system over an extended period

Tools being considered:
- Locust or JMeter for load testing
- Benchmark tools for specific API endpoint performance testing

## CI/CD Integration

- Regular tests run on every build
- Builds fail if tests fail or coverage drops below threshold
- Contract tests run:
  - On a scheduled basis (weekly)
  - Manually before releases
  - When investigating integration issues

## Best Practices for Writing Tests

1. **Descriptive Test Names**: Use clear, descriptive test names that explain what's being tested
   ```python
   def test_average_temperature_calculation_rounds_to_one_decimal():
       # Test code
   ```

2. **Arrange-Act-Assert Pattern**: Structure tests with clear sections
   ```python
   def test_something():
       # Arrange - set up test data
       data = {...}
       
       # Act - call the function being tested
       result = function_under_test(data)
       
       # Assert - verify the results
       assert result == expected_output
   ```

3. **One Assertion Per Test**: Focus each test on verifying one thing

4. **Use Test Data Factories**: Create helper functions for generating test data

5. **Mock External Dependencies**: Don't rely on external services for unit tests

## Future Testing Improvements

1. Add more integration tests for the full request/response cycle
2. Add performance tests for critical endpoints
3. Expand contract testing to cover more edge cases
4. Add load testing for high-traffic scenarios
5. Standardize remaining tests to use pytest consistently
6. Refactor Django TestCase-based tests to use pytest fixtures
7. Implement frontend testing suite once implementation begins

> **Legend:**  
> ✅ Implemented - Feature is complete and working  
> 🚧 In Progress - Feature is partially implemented  
> 📝 Planned - Feature is planned but not yet implemented