from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from geopy.geocoders import Nominatim
from .models import Trip  
from .serializers import TripSerializer  
import logging
import time

# Initialize geocoder
geolocator = Nominatim(user_agent="test/1.0 (hamza.dridi.1@esprit.tn)")
# Setup logging
logger = logging.getLogger(__name__)

class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer

    def get_coordinates(self, location_name):
        """Get latitude and longitude for a given location"""
        if location_name:
            try:
                location = geolocator.geocode(location_name)
                if location:
                    return location.latitude, location.longitude
                else:
                    logger.error(f"Could not find coordinates for location: {location_name}")
            except Exception as e:
                logger.error(f"Error geocoding location {location_name}: {e}")
        return None, None  # Return None if not found or error occurs

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            trip = serializer.save()

            # Get Lat/Lng for each location
            trip.current_latitude, trip.current_longitude = self.get_coordinates(trip.current_location)
            trip.pickup_latitude, trip.pickup_longitude = self.get_coordinates(trip.pickup_location)
            trip.dropoff_latitude, trip.dropoff_longitude = self.get_coordinates(trip.dropoff_location)

            # Save the updated trip with coordinates
            trip.save()

            # Logging the trip details
            logger.info(f"🚀 New Trip Created!")
            logger.info(f"📍 Current Location: {trip.current_location} (Lat: {trip.current_latitude}, Lng: {trip.current_longitude})")
            logger.info(f"🚖 Pickup Location: {trip.pickup_location} (Lat: {trip.pickup_latitude}, Lng: {trip.pickup_longitude})")
            logger.info(f"🏁 Dropoff Location: {trip.dropoff_location} (Lat: {trip.dropoff_latitude}, Lng: {trip.dropoff_longitude})")
            logger.info(f"🔄 Cycle Used: {trip.current_cycle_used} hours")

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)