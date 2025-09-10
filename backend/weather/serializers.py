from rest_framework import serializers
from .models import WeatherData

class WeatherDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherData
        fields = ['id', 'city', 'date', 'temperature', 'timestamp']
        read_only_fields = ['timestamp']

class WeatherAverageRequestSerializer(serializers.Serializer):
    city = serializers.CharField(max_length=100)
    days = serializers.IntegerField(min_value=1, max_value=30)
    
class WeatherAverageResponseSerializer(serializers.Serializer):
    city = serializers.CharField()
    average_temperature = serializers.FloatField()
    days = serializers.IntegerField()
    start_date = serializers.DateField()
    end_date = serializers.DateField()
