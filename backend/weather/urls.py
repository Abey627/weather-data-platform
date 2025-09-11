from django.urls import path
from .views import WeatherAverageView, WeatherDataListView

urlpatterns = [
    path('average', WeatherAverageView.as_view(), name='weather_average'),
    path('history', WeatherDataListView.as_view(), name='weather_history'),
]
