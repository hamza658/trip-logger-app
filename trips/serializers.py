from rest_framework import serializers
from .models import Trip
from django.utils import timezone

class TripSerializer(serializers.ModelSerializer):
    # Add a custom read-only field for formatted trip date
    formatted_trip_date = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Trip
        fields = [
            'id',
            'current_location', 'current_latitude', 'current_longitude',
            'pickup_location', 'pickup_latitude', 'pickup_longitude',
            'dropoff_location', 'dropoff_latitude', 'dropoff_longitude',
            'current_cycle_used',
            'trip_date', 'formatted_trip_date',
            'created_at', 'updated_at'
        ]
    
    def get_formatted_trip_date(self, obj):
        """Convert datetime to date-only string format"""
        if isinstance(obj.trip_date, timezone.datetime):
            return obj.trip_date.date().isoformat()
        return obj.trip_date.isoformat() if obj.trip_date else None
    
    def validate_current_cycle_used(self, value):
        if value < 0:
            raise serializers.ValidationError("Cycle used cannot be negative.")
        return value