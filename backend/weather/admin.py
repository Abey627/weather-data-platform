from django.contrib import admin
from .models import WeatherData

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ('city', 'date', 'temperature', 'timestamp')
    list_filter = ('city', 'date')
    search_fields = ('city',)
    ordering = ('-date',)
