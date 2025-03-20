from django.db import models
from django.utils import timezone

class Trip(models.Model):
    current_location = models.CharField(max_length=255)
    current_latitude = models.FloatField(null=True, blank=True)
    current_longitude = models.FloatField(null=True, blank=True)
    
    pickup_location = models.CharField(max_length=255)
    pickup_latitude = models.FloatField(null=True, blank=True)
    pickup_longitude = models.FloatField(null=True, blank=True)
    
    dropoff_location = models.CharField(max_length=255)
    dropoff_latitude = models.FloatField(null=True, blank=True)
    dropoff_longitude = models.FloatField(null=True, blank=True)
    
    current_cycle_used = models.PositiveIntegerField()
    
    # Using date field explicitly instead of datetime
    trip_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Trip from {self.pickup_location} to {self.dropoff_location}"


class ELDLog(models.Model):
    trip = models.ForeignKey(Trip, related_name='eld_logs', on_delete=models.CASCADE)
    log_date = models.DateField()
    hours_driven = models.FloatField()
    rests_taken = models.IntegerField()
    fuel_stops = models.IntegerField()
    
    record_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"ELD Log for {self.trip}"