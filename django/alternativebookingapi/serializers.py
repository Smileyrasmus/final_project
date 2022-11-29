from .models import Order, Event, Booking, Location, BookableItem
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    created_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    updated_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    user = serializers.ReadOnlyField(source="created_by.username")
    user_link = serializers.HyperlinkedRelatedField(
        view_name="user-detail", read_only=True, source="created_by"
    )

    def _user(self, obj):
        request = self.context.get("request", None)
        if request:
            return request.user

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

    def save(self, **kwargs):
        user = self._user(self)
        if user.conditions["order"]["must_have_customer_id"]:
            if not self.validated_data.get("customer_id"):
                raise serializers.ValidationError(
                    {"customer_id": "Customer ID is required"}
                )
        return super().save(**kwargs)


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

        def save(self, **kwargs):
            user = self._user(self)
            event = self.validated_data.get("event")
            order = self.validated_data.get("order")
            if user.conditions["booking"]["require_bookable_item"]:
                if not self.validated_data.get("bookable_item"):
                    raise serializers.ValidationError(
                        {"bookable_item": "Bookable item is required"}
                    )
            if user.conditions["booking"]["duplicate_bookings"]:
                if Booking.objects.filter(
                    event=event, created_by=user, order=order
                ).exists():
                    raise serializers.ValidationError(
                        {"bookable_item": "Booking already exists"}
                    )
            if not self.validated_data.get("bookable_item").active:
                raise serializers.ValidationError(
                    {"bookable_item": "Bookable item is not active"}
                )
            return super().save(**kwargs)


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

        def save(self, *args, **kwargs):
            user = self._user(self)
            name = self.validated_data.get("name")
            start_time = self.validated_data.get("start_time")
            end_time = self.validated_data.get("end_time")
            location = self.validated_data.get("location")
            id = self.validated_data.get("id")
            if user.conditions["event"]["duplicate_event"]:
                if Event.objects.filter(
                    name=name,
                    start_time=start_time,
                    end_time=end_time,
                    created_by=user,
                ).exists():
                    raise serializers.ValidationError({"name": "Event already exists"})

            if user.conditions["event"]["start_end_overlay"] and id:
                if (
                    Event.objects.filter(
                        start_time__lte=start_time,
                        end_time__gte=end_time,
                        created_by=user,
                    )
                    .exclude(id=id)
                    .exists()
                ):
                    raise serializers.ValidationError(
                        {"name": "Event start and end time overlap"}
                    )

            if user.conditions["event"]["start_end_overlay"]:
                if Event.objects.filter(
                    location=location,
                    start_time__lte=start_time,
                    end_time__gte=end_time,
                    created_by=user,
                ).exists():
                    raise serializers.ValidationError(
                        {"name": "Event overlaps existing event"}
                    )
            return super().save(**kwargs)


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

    def save(self, *args, **kwargs):
        user = self._user(self)
        name = self.context["request"].data["name"]
        if (
            user.conditions["location"]["duplicate_location"]
            and Location.objects.filter(name=name, created_by=user).exists()
        ):
            raise serializers.ValidationError("Location with this name already exists")
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        user = self._user(self)
        name = self.context["request"].data["name"]
        if user.conditions["bookable_item"]["duplicate_bookable_item"]:
            if BookableItem.objects.filter(name=name, created_by=user).exists():
                raise serializers.ValidationError(
                    "Bookable item with this name already exists"
                )
        super().save(*args, **kwargs)
