import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from django.core.cache import cache
from weather.utils.date_utils import get_date_range
from weather.utils.cache_utils import CacheManager
from weather.utils.error_handlers import handle_api_exception
from rest_framework.response import Response
from rest_framework import status

class TestDateUtils:
    """Tests for date_utils.py"""
    
    @patch('weather.utils.date_utils.datetime')
    def test_get_date_range(self, mock_datetime):
        """Test calculation of date range"""
        # Setup a fixed current date for consistent testing
        fixed_date = datetime(2025, 9, 12)
        mock_datetime.now.return_value = fixed_date
        
        # Test with different day values
        test_cases = [
            (3, (datetime(2025, 9, 9).date(), datetime(2025, 9, 12).date())),
            (7, (datetime(2025, 9, 5).date(), datetime(2025, 9, 12).date())),
            (30, (datetime(2025, 8, 13).date(), datetime(2025, 9, 12).date())),
        ]
        
        for days_back, expected_range in test_cases:
            start_date, end_date = get_date_range(days_back)
            assert start_date == expected_range[0]
            assert end_date == expected_range[1]
        
        # Verify the datetime.now() was called
        mock_datetime.now.assert_called()

class TestCacheUtils:
    """Tests for cache_utils.py"""
    
    @patch('weather.utils.cache_utils.cache.get_or_set')
    def test_get_or_set(self, mock_cache_get_or_set):
        """Test the get_or_set method"""
        # Setup
        key = "test_key"
        value = "test_value"
        timeout = 3600
        
        # Configure the mock
        mock_cache_get_or_set.return_value = value
        
        # Create a getter function
        def getter_func():
            return value
        
        # Call the method
        result = CacheManager.get_or_set(key, getter_func, timeout)
        
        # Verify
        assert result == value
        mock_cache_get_or_set.assert_called_once_with(key, getter_func, timeout)

class TestErrorHandlers:
    """Tests for error_handlers.py"""
    
    def test_handle_api_exception_no_error(self):
        """Test the decorator when no error occurs"""
        # Setup
        @handle_api_exception
        def test_func():
            return Response({"message": "success"}, status=status.HTTP_200_OK)
        
        # Call the decorated function
        response = test_func()
        
        # Verify
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {"message": "success"}
    
    def test_handle_api_exception_value_error(self):
        """Test the decorator with a ValueError"""
        # Setup
        @handle_api_exception
        def test_func():
            raise ValueError("Test error message")
        
        # Call the decorated function
        response = test_func()
        
        # Verify
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Test error message" in str(response.data)
    
    def test_handle_api_exception_generic_exception(self):
        """Test the decorator with a generic Exception"""
        # Setup
        @handle_api_exception
        def test_func():
            raise Exception("Internal server error")
        
        # Call the decorated function
        response = test_func()
        
        # Verify
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "unexpected error" in str(response.data["error"]).lower()