from django.urls import path
from .views import WeatherAverageView

urlpatterns = [
    path('average', WeatherAverageView.as_view(), name='weather_average'),
]
