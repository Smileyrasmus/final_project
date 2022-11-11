from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bookingapi.models import *


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
        fields = ['url', 'id', 'name', 'description', 'user']
        read_only_fields = ['user']


class SeatSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = Seat
        fields = ['url', 'id', 'name', 'description',
                  'restricted', 'bookable_location', 'user']
        read_only_fields = ['user']


class LocationBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = LocationBooking
        fields = ['url', 'id', 'bookable_location',
                  'start_time', 'end_time', 'event_name', 'event_description', 'user']
        read_only_fields = ['user']


class SeatBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = SeatBooking
        fields = ['url', 'id', 'customer', 'seat', 'location_booking', 'user']
        read_only_fields = ['user']
