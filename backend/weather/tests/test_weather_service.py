import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, date
from weather.integration.services.weather import WeatherService
from weather.models import WeatherData

@pytest.fixture
def sample_weather_data():
    """Fixture to provide sample weather data"""
    return [
        {"date": "2025-09-10", "temperature": 25.5},
        {"date": "2025-09-11", "temperature": 26.8},
        {"date": "2025-09-12", "temperature": 24.3},
    ]

@pytest.fixture
def raw_weather_api_response():
    """Fixture to provide a sample response from the weather API"""
    return {
        "latitude": 40.71,
        "longitude": -74.01,
        "timezone": "America/New_York",
        "daily": {
            "time": ["2025-09-10", "2025-09-11", "2025-09-12"],
            "temperature_2m_max": [25.5, 26.8, 24.3]
        }
    }

@pytest.mark.django_db
class TestWeatherService:
    """Tests for WeatherService"""
    
    def test_process_weather_data(self, raw_weather_api_response, sample_weather_data):
        """Test processing of raw weather data"""
        processed_data = WeatherService._process_weather_data(raw_weather_api_response)
        assert processed_data == sample_weather_data
    
    def test_calculate_average_temperature(self, sample_weather_data):
        """Test calculation of average temperature"""
        avg_temp = WeatherService.calculate_average_temperature(sample_weather_data)
        expected_avg = round((25.5 + 26.8 + 24.3) / 3, 2)
        assert avg_temp == expected_avg
    
    def test_calculate_average_temperature_empty_data(self):
        """Test calculation of average temperature with empty data"""
        avg_temp = WeatherService.calculate_average_temperature([])
        assert avg_temp == 0
    
    @patch('weather.integration.services.weather.WeatherData.objects.filter')
    def test_get_weather_from_db(self, mock_filter):
        """Test fetching weather data from the database"""
        # Setup mock data
        city = "New York"
        start_date = date(2025, 9, 10)
        end_date = date(2025, 9, 12)
        
        # Create mock weather data objects with proper date strings
        mock_data = []
        for d, temp in [
            (date(2025, 9, 10), 25.5),
            (date(2025, 9, 11), 26.8),
            (date(2025, 9, 12), 24.3)
        ]:
            mock_obj = MagicMock()
            mock_obj.city = city
            mock_obj.date = MagicMock()
            mock_obj.date.strftime = lambda fmt, d=d: d.strftime(fmt)
            mock_obj.temperature = temp
            mock_data.append(mock_obj)
        
        # Configure the filter mock
        mock_filter.return_value.order_by.return_value = mock_data
        
        # Call the method
        result = WeatherService.get_weather_from_db(city, start_date, end_date)
        
        # Assert the filter was called with correct parameters
        mock_filter.assert_called_once_with(
            city=city,
            date__gte=start_date,
            date__lte=end_date
        )
        
        # Verify the result
        expected_result = [
            {"date": "2025-09-10", "temperature": 25.5},
            {"date": "2025-09-11", "temperature": 26.8},
            {"date": "2025-09-12", "temperature": 24.3},
        ]
        assert result == expected_result
    
    @pytest.mark.django_db
    def test_store_weather_data(self, sample_weather_data):
        """Test storing weather data in the database"""
        city = "New York"
        
        # Ensure no data exists before the test
        WeatherData.objects.all().delete()
        
        # Call the method
        stored_data = WeatherService.store_weather_data(city, sample_weather_data)
        
        # Verify data was stored
        assert len(stored_data) == 3
        
        # Check the database records
        db_records = WeatherData.objects.filter(city=city).order_by('date')
        assert db_records.count() == 3
        
        # Verify the data matches
        for i, record in enumerate(db_records):
            assert record.city == city
            assert record.date.strftime("%Y-%m-%d") == sample_weather_data[i]["date"]
            assert record.temperature == sample_weather_data[i]["temperature"]
    
    @pytest.mark.django_db
    def test_store_weather_data_update_existing(self, sample_weather_data):
        """Test updating existing weather data in the database"""
        city = "New York"
        
        # Create initial data
        WeatherData.objects.create(
            city=city,
            date=datetime.strptime(sample_weather_data[0]["date"], "%Y-%m-%d").date(),
            temperature=20.0  # Different temperature to test update
        )
        
        # Call the method
        stored_data = WeatherService.store_weather_data(city, sample_weather_data)
        
        # Verify data was stored
        assert len(stored_data) == 3
        
        # Check the database records
        db_records = WeatherData.objects.filter(city=city).order_by('date')
        assert db_records.count() == 3
        
        # Verify the first record was updated
        first_record = db_records.first()
        assert first_record.temperature == sample_weather_data[0]["temperature"]
    
    @patch('weather.integration.services.weather.GeocodingService.get_coordinates')
    @patch('weather.integration.services.weather.WeatherClient.get_historical_weather')
    @patch('weather.integration.services.weather.CacheManager.get_or_set')
    def test_get_historical_weather_from_api(self, mock_cache, mock_weather_client, mock_geocoding):
        """Test fetching historical weather data from the API"""
        # Setup
        city = "New York"
        days = 3
        
        # Configure the geocoding mock
        mock_geocoding.return_value = {"latitude": 40.71, "longitude": -74.01}
        
        # Configure the weather client mock
        raw_data = {
            "daily": {
                "time": ["2025-09-10", "2025-09-11", "2025-09-12"],
                "temperature_2m_max": [25.5, 26.8, 24.3]
            }
        }
        mock_weather_client.return_value = raw_data
        
        # Configure the cache mock to call the real function
        def cache_side_effect(key, func, timeout):
            return func()
        
        mock_cache.side_effect = cache_side_effect
        
        # Call the method
        with patch('weather.integration.services.weather.WeatherService.get_weather_from_db') as mock_db:
            # Make the database return empty results to force API call
            mock_db.return_value = []
            
            with patch('weather.integration.services.weather.WeatherService.store_weather_data') as mock_store:
                result = WeatherService.get_historical_weather(city, days)
        
        # Verify the result
        expected_result = [
            {"date": "2025-09-10", "temperature": 25.5},
            {"date": "2025-09-11", "temperature": 26.8},
            {"date": "2025-09-12", "temperature": 24.3},
        ]
        assert result == expected_result
        
        # Verify the geocoding service was called
        mock_geocoding.assert_called_once_with(city)
        
        # Verify the weather client was called with correct parameters
        mock_weather_client.assert_called_once()
    
    @patch('weather.integration.services.weather.GeocodingService.get_coordinates')
    def test_get_historical_weather_geocoding_error(self, mock_geocoding):
        """Test error handling when geocoding fails"""
        # Setup
        city = "NonExistentCity"
        days = 3
        
        # Configure the geocoding mock to raise an error
        mock_geocoding.side_effect = ValueError("Could not find coordinates for city")
        
        # Call the method and expect an error
        with pytest.raises(ValueError) as excinfo:
            with patch('weather.integration.services.weather.CacheManager.get_or_set') as mock_cache:
                # Make the cache call the real function
                def cache_side_effect(key, func, timeout):
                    return func()
                
                mock_cache.side_effect = cache_side_effect
                
                WeatherService.get_historical_weather(city, days)
        
        # Verify the error message
        assert "Could not find coordinates for city" in str(excinfo.value)
        
        # Verify the geocoding service was called
        mock_geocoding.assert_called_once_with(city)