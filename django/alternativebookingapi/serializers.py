from .models import Order, Event, Booking, Location, BookableItem
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )

    class Meta:
        abstract = True


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class OrderSerializer(BaseSerializer):
    class Meta:
        model = Order
        fields = [
            "url",
            "id",
            "user",
            "created_by",
            "user_link",
            "note",
            "bookings",
        ]
        read_only_fields = ["bookings"]


class BookingSerializer(BaseSerializer):
    class Meta:
        model = Booking
        fields = [
            "url",
            "id",
            "created_by",
            "user",
            "user_link",
            "order",
            "event",
            "bookable_item",
        ]


class EventSerializer(BaseSerializer):
    class Meta:
        model = Event
        fields = [
            "url",
            "id",
            "created_by",
            "user",
            "user_link",
            "name",
            "description",
            "locations",
            "start_time",
            "end_time",
        ]


class LocationSerializer(BaseSerializer):
    class Meta:
        model = Location
        fields = [
            "url",
            "id",
            "user",
            "created_by",
            "user_link",
            "name",
            "description",
            "events",
        ]


class BookableItemSerializer(BaseSerializer):
    class Meta:
        model = BookableItem
        fields = [
            "url",
            "id",
            "user",
            "created_by",
            "user_link",
            "name",
            "description",
            "active",
            "location",
        ]
