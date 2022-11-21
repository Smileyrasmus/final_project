from .models import Order, Event, Booking, Location, BookableItem
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )

    class Meta:
        abstract = True


class OrderSerializer(BaseSerializer):
    booking = serializers.SerializerMethodField()

    def get_booking(self, obj):
        return {
            "bookings": obj.bookings.all().values(
                "id",
                "bookable_item__name",
                "event__name",
                "event__start_time",
                "event__end_time",
                "bookable_item__location__name",
            ),
        }

    class Meta:
        model = Order
        fields = [
            "url",
            "id",
            "user",
            "created_by",
            "user_link",
            "customer_id",
            "note",
            "booking",
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
