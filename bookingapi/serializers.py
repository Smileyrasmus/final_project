from django.contrib.auth.models import User, Group
from rest_framework import serializers

from bookingapi.models import BookableLocation, Seat, LocationBooking, SeatBooking, Row, Section


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
        fields = ['url', 'name', 'description', 'user', 'created_by']
        read_only_fields = ['created_by']

class SeatSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Seat
        fields = ['url', 'description', 'row', 'restricted', 'name', 'user', 'created_by']
        read_only_fields = ['created_by']

class LocationBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = LocationBooking
        fields = ['url', 'bookable_location', 'start_time', 'end_time', 'event', 'user', 'created_by']
        read_only_fields = ['created_by']
        
class SeatBookingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = SeatBooking
        fields = ['url', 'customer', 'seat', 'user', 'created_by']
        read_only_fields = ['created_by']

class SectionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Section
        fields = ['url', 'description', 'name', 'bookable_location', 'user', 'created_by']
        read_only_fields = ['created_by']

class RowSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='created_by.username')
    class Meta:
        model = Row
        fields = ['url', 'description', 'name', 'section', 'user', 'created_by']
        read_only_fields = ['created_by']