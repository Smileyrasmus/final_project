from .models import Order, Event, Booking, Location, BookableItem
from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "groups"]


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ["url", "name"]


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )
    event_link = serializers.HyperlinkedRelatedField(
        view_name="event-detail", read_only=True
    )

    class Meta:
        model = Order
        fields = [
            "url",
            "id",
            "user",
            "user_link",
            "event_link",
            "note",
        ]


class EventSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )
    location_links = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="location-detail"
    )

    class Meta:
        model = Event
        fields = [
            "url",
            "id",
            "user",
            "user_link",
            "name",
            "description",
            "locations",
            "location_links",
            "start_time",
            "end_time",
        ]


class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )
    event_link = serializers.HyperlinkedRelatedField(
        view_name="event-detail", read_only=True
    )
    order_link = serializers.HyperlinkedRelatedField(
        view_name="order-detail", read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            "url",
            "id",
            "user",
            "user_link",
            "order",
            "order_link",
            "event",
            "event_link",
        ]


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )
    bookable_item_link = serializers.HyperlinkedRelatedField(
        view_name="bookableitem-detail", read_only=True
    )
    event_links = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="event-detail"
    )

    class Meta:
        model = Location
        fields = [
            "url",
            "id",
            "user",
            "user_link",
            "name",
            "description",
            "bookable_item_link",
            "events",
            "event_links",
        ]


class BookableItemSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )
    location_link = serializers.HyperlinkedRelatedField(
        view_name="location-detail", read_only=True
    )

    class Meta:
        model = BookableItem
        fieds = [
            "url",
            "id",
            "user",
            "user_link",
            "name",
            "description",
            "active",
            "location",
            "location_link",
        ]
