import pytest
import os
import json
import jsonschema
from datetime import date, timedelta
from weather.integration.clients.weather import WeatherClient
from weather.utils.constants import WEATHER_API_BASE_URL

# Path to store the contract files
CONTRACT_DIR = os.path.join(os.path.dirname(__file__), 'contracts')
WEATHER_CONTRACT_FILE = os.path.join(CONTRACT_DIR, 'weather_api_response.json')
WEATHER_SCHEMA_FILE = os.path.join(CONTRACT_DIR, 'weather_api_schema.json')

# Expected schema for the weather API response
WEATHER_API_SCHEMA = {
    "type": "object",
    "required": ["latitude", "longitude", "timezone", "daily"],
    "properties": {
        "latitude": {"type": "number"},
        "longitude": {"type": "number"},
        "timezone": {"type": "string"},
        "daily": {
            "type": "object",
            "required": ["time", "temperature_2m_max"],
            "properties": {
                "time": {
                    "type": "array",
                    "items": {"type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$"}
                },
                "temperature_2m_max": {
                    "type": "array",
                    "items": {"type": "number"}
                }
            }
        }
    }
}

# Ensure contract directory exists
os.makedirs(CONTRACT_DIR, exist_ok=True)

# Save the schema if it doesn't exist
if not os.path.exists(WEATHER_SCHEMA_FILE):
    with open(WEATHER_SCHEMA_FILE, 'w') as f:
        json.dump(WEATHER_API_SCHEMA, f, indent=2)


@pytest.mark.contract
class TestWeatherApiContract:
    """Contract tests for the Weather API.
    
    These tests make actual API calls and should be run in a controlled environment,
    not in regular CI/CD pipelines.
    
    Run with: pytest -m contract
    """
    
    @pytest.fixture
    def weather_api_response(self):
        """Make an actual API call and return the response"""
        # New York coordinates
        latitude = 40.71
        longitude = -74.01
        
        # Calculate date range for last 7 days
        end_date = date.today()
        start_date = end_date - timedelta(days=7)
        
        # Make the actual API call
        response = WeatherClient.get_historical_weather(
            latitude, 
            longitude, 
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d"),
            _skip_cache=True  # Bypass cache to ensure a real API call
        )
        
        return response
    
    def test_weather_api_schema_compliance(self, weather_api_response):
        """Test that the API response complies with our expected schema"""
        try:
            # Validate against the schema
            jsonschema.validate(instance=weather_api_response, schema=WEATHER_API_SCHEMA)
            
            # If validation passes, update the contract file
            with open(WEATHER_CONTRACT_FILE, 'w') as f:
                json.dump(weather_api_response, f, indent=2)
                
            print("\nWeather API contract updated successfully.")
            
        except jsonschema.exceptions.ValidationError as e:
            # If the schema has changed, this will help understand what changed
            print(f"\nSchema validation failed: {e}")
            
            # If we have a stored contract, compare with it
            if os.path.exists(WEATHER_CONTRACT_FILE):
                with open(WEATHER_CONTRACT_FILE, 'r') as f:
                    stored_contract = json.load(f)
                
                # Compare key differences (this is a simple comparison,
                # real projects might use more sophisticated diff tools)
                print("\nDifferences from stored contract:")
                self._compare_contracts(stored_contract, weather_api_response)
            
            # Re-raise the exception to fail the test
            raise
    
    def test_weather_response_field_values(self, weather_api_response):
        """Test that specific fields have expected value types and ranges"""
        # Check that latitude is within valid range
        assert -90 <= weather_api_response["latitude"] <= 90, "Latitude should be between -90 and 90"
        
        # Check that longitude is within valid range
        assert -180 <= weather_api_response["longitude"] <= 180, "Longitude should be between -180 and 180"
        
        # Check that temperature values are within reasonable ranges
        for temp in weather_api_response["daily"]["temperature_2m_max"]:
            assert -100 <= temp <= 100, f"Temperature {temp} should be in a reasonable range"
        
        # Check that the number of dates matches the number of temperature readings
        assert len(weather_api_response["daily"]["time"]) == len(weather_api_response["daily"]["temperature_2m_max"]), \
            "The number of dates should match the number of temperature readings"
    
    def _compare_contracts(self, old_contract, new_contract, path=""):
        """Recursively compare two contracts and print differences"""
        if isinstance(old_contract, dict) and isinstance(new_contract, dict):
            # Check for missing or added keys
            old_keys = set(old_contract.keys())
            new_keys = set(new_contract.keys())
            
            for key in old_keys - new_keys:
                print(f"  Key removed: {path}/{key}")
            
            for key in new_keys - old_keys:
                print(f"  Key added: {path}/{key}")
            
            # Check values of common keys
            for key in old_keys.intersection(new_keys):
                self._compare_contracts(old_contract[key], new_contract[key], f"{path}/{key}")
                
        elif isinstance(old_contract, list) and isinstance(new_contract, list):
            # For lists, just check length for simplicity
            if len(old_contract) != len(new_contract):
                print(f"  List length changed at {path}: {len(old_contract)} -> {len(new_contract)}")
                
        elif old_contract != new_contract:
            # For simple values, just show the change
            print(f"  Value changed at {path}: {old_contract} -> {new_contract}")