from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import WeatherAverageRequestSerializer, WeatherAverageResponseSerializer
from .services import WeatherService
from datetime import datetime, timedelta

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
    def get(self, request):
        # Validate request parameters
        serializer = WeatherAverageRequestSerializer(data=request.query_params)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        city = serializer.validated_data['city']
        days = serializer.validated_data['days']
        
        try:
            # Get weather data
            weather_data = WeatherService.get_historical_weather(city, days)
            
            # Calculate average temperature
            avg_temp = WeatherService.calculate_average_temperature(weather_data)
            
            # Prepare response
            end_date = datetime.now().date()
            start_date = end_date - timedelta(days=days)
            
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
            
        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
