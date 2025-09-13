from django.urls import path
from django.http import HttpResponse
from .views import WeatherAverageView, WeatherDataListView

# Simple health check view for monitoring
def health_check(request):
    return HttpResponse("OK")

urlpatterns = [
    path('average', WeatherAverageView.as_view(), name='weather_average'),
    path('history', WeatherDataListView.as_view(), name='weather_history'),
    path('health/', health_check, name='health_check'),
]
