from django.db import models

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    date = models.DateField()
    temperature = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('city', 'date')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.city} - {self.date} - {self.temperature}°C"
