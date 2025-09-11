from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import WeatherData
from .serializers import (
    WeatherAverageRequestSerializer, 
    WeatherAverageResponseSerializer,
    WeatherDataSerializer
)
from .integration.services.weather import WeatherService
from .utils.date_utils import get_date_range
from .utils.error_handlers import handle_api_exception

class WeatherAverageView(APIView):
    """
    API view to get average temperature for a city over a specified number of days
    """
    
    @swagger_auto_schema(
        operation_description="Get average temperature for a city over a specified number of days",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, description="City name", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('days', openapi.IN_QUERY, description="Number of days", type=openapi.TYPE_INTEGER, required=True),
        ],
        responses={
            200: WeatherAverageResponseSerializer,
            400: "Bad request",
            500: "Internal server error"
        }
    )
    @handle_api_exception
    def get(self, request):
        # Validate request parameters
        serializer = WeatherAverageRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Get validated parameters
        city = serializer.validated_data['city']
        days = serializer.validated_data['days']
        
        # Process the request
        return self._process_weather_request(city, days)
            
    def _process_weather_request(self, city, days):
        """
        Process weather request for a city and number of days
        
        Args:
            city (str): City name
            days (int): Number of days
            
        Returns:
            Response: Django REST framework response
        """
        # Get weather data
        weather_data = WeatherService.get_historical_weather(city, days)
        
        # Calculate average temperature
        avg_temp = WeatherService.calculate_average_temperature(weather_data)
        
        # Get date range
        start_date, end_date = get_date_range(days)
        
        # Prepare and validate response
        response_data = {
            'city': city,
            'average_temperature': avg_temp,
            'days': days,
            'start_date': start_date,
            'end_date': end_date
        }
        
        response_serializer = WeatherAverageResponseSerializer(data=response_data)
        response_serializer.is_valid(raise_exception=True)
        
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class WeatherDataListView(generics.ListAPIView):
    """
    API view to list historical weather data from the database
    """
    serializer_class = WeatherDataSerializer
    
    @swagger_auto_schema(
        operation_description="Get historical weather data for a city",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, description="City name (optional)", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Start date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="End date (YYYY-MM-DD)", type=openapi.TYPE_STRING),
        ],
    )
    def get_queryset(self):
        """
        Filter the queryset based on query parameters
        """
        queryset = WeatherData.objects.all()
        
        # Apply filters if provided
        city = self.request.query_params.get('city')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if city:
            queryset = queryset.filter(city__icontains=city)
        
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date')
