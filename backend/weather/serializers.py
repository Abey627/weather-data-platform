from rest_framework import serializers
from .models import WeatherData
from .utils.constants import MAX_DAYS_ALLOWED

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['id', 'city', 'date', 'temperature', 'timestamp']
        read_only_fields = ['timestamp']

class WeatherAverageRequestSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    days = serializers.IntegerField(min_value=1, max_value=MAX_DAYS_ALLOWED)
    
class WeatherAverageResponseSerializer(serializers.Serializer):
    city = serializers.CharField()
    average_temperature = serializers.FloatField()
    days = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
