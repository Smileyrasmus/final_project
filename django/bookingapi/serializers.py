from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bookingapi.models import BookableLocation, Seat, LocationBooking, SeatBooking, Event


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class BookableLocationSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = BookableLocation
        fields = ['url', 'name', 'description', 'user']

class EventSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Event
        fields = ['url', 'name', 'description', 'user']

class SeatSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Seat
        fields = ['url', 'name', 'description', 'restricted', 'bookable_location', 'user']

class LocationBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = LocationBooking
        fields = ['url', 'bookable_location', 'start_time', 'end_time', 'event', 'user']
        
class SeatBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = SeatBooking
        fields = ['url', 'customer', 'seat', 'location_booking', 'user']