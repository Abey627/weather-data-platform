import pytest
import os
import json
import jsonschema
from weather.integration.clients.geocoding import GeocodingClient

# Path to store the contract files
CONTRACT_DIR = os.path.join(os.path.dirname(__file__), 'contracts')
GEOCODING_CONTRACT_FILE = os.path.join(CONTRACT_DIR, 'geocoding_api_response.json')
GEOCODING_SCHEMA_FILE = os.path.join(CONTRACT_DIR, 'geocoding_api_schema.json')

# Expected schema for the geocoding API response
GEOCODING_API_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "required": ["lat", "lon", "name"],
        "properties": {
            "lat": {"type": "string", "pattern": "^-?\\d+(\\.\\d+)?$"},  # String that can be converted to float
            "lon": {"type": "string", "pattern": "^-?\\d+(\\.\\d+)?$"},  # String that can be converted to float
            "name": {"type": "string"},
            "country": {"type": "string"}
        }
    }
}

# Ensure contract directory exists
os.makedirs(CONTRACT_DIR, exist_ok=True)

# Save the schema if it doesn't exist
if not os.path.exists(GEOCODING_SCHEMA_FILE):
    with open(GEOCODING_SCHEMA_FILE, 'w') as f:
        json.dump(GEOCODING_API_SCHEMA, f, indent=2)


@pytest.mark.contract
class TestGeocodingApiContract:
    """Contract tests for the Geocoding API.
    
    These tests make actual API calls and should be run in a controlled environment,
    not in regular CI/CD pipelines.
    
    Run with: pytest -m contract
    """
    
    @pytest.fixture
    def geocoding_api_response(self):
        """Make an actual API call and return the response"""
        # Well-known city that should always exist
        city = "New York"
        
        # Use internal method to make direct API call
        return GeocodingClient._make_geocoding_request(city)
    
    def test_geocoding_api_schema_compliance(self, geocoding_api_response):
        """Test that the API response complies with our expected schema"""
        try:
            # Validate against the schema
            jsonschema.validate(instance=geocoding_api_response, schema=GEOCODING_API_SCHEMA)
            
            # If validation passes, update the contract file
            with open(GEOCODING_CONTRACT_FILE, 'w') as f:
                json.dump(geocoding_api_response, f, indent=2)
                
            print("\nGeocoding API contract updated successfully.")
            
        except jsonschema.exceptions.ValidationError as e:
            # If the schema has changed, this will help understand what changed
            print(f"\nSchema validation failed: {e}")
            
            # If we have a stored contract, compare with it
            if os.path.exists(GEOCODING_CONTRACT_FILE):
                with open(GEOCODING_CONTRACT_FILE, 'r') as f:
                    stored_contract = json.load(f)
                
                # Compare key differences
                print("\nDifferences from stored contract:")
                self._compare_contracts(stored_contract, geocoding_api_response)
            
            # Re-raise the exception to fail the test
            raise
    
    def test_geocoding_response_field_values(self, geocoding_api_response):
        """Test that specific fields have expected value types and ranges"""
        # Check that we got at least one result
        assert len(geocoding_api_response) > 0, "Geocoding API should return at least one result"
        
        # Check the first result
        first_result = geocoding_api_response[0]
        
        # Check that latitude is within valid range
        lat = float(first_result["lat"])
        assert -90 <= lat <= 90, "Latitude should be between -90 and 90"
        
        # Check that longitude is within valid range
        lon = float(first_result["lon"])
        assert -180 <= lon <= 180, "Longitude should be between -180 and 180"
        
        # Check that name is not empty
        assert first_result["name"], "Name should not be empty"
    
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