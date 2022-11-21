from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True


class Order(BaseModel):
    customer_id = models.CharField(max_length=255, null=True, blank=True)
    note = models.CharField(max_length=255, blank=True, null=True)

    def clean(self):
        if (
            self.customer_id is None
            and User.conditions["order"]["must_have_customer_id"]
        ):
            raise ValidationError("Customer id must be set")


class Event(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if (
            self.start_time >= self.end_time
            and User.conditions["event"]["start_end_overlay"]
        ):
            raise ValidationError("Start time must be before end time")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["name", "created_by", "start_time", "end_time"],
    #             name="unique_event",
    #             condition=models.Q()
    #             violation_error_message="Event already exists",
    #         )
    #     ]


class Location(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    events = models.ManyToManyField("Event", related_name="locations", blank=True)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["name", "created_by"],
    #             name="unique_location",
    #             condition=models.Q(
    #                 User.conditions.keys()["location"]["dublicate_location"]
    #             ),
    #             violation_error_message="Location with this name already exists",
    #         )
    #     ]


class BookableItem(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="seats", null=True, blank=True
    )

    def clean(self):
        if self.active == False and User.conditions["bookable_item"]["active"] == True:
            raise ValidationError("Bookable item is not active")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["name", "location", "created_by"],
    #             name="unique_item_name_for_location",
    #             condition=models.Q(
    #                 User.conditions["bookable_item"]["dublicate_bookable_item"] == True
    #             ),
    #             violation_error_message="Item already attributed for this location",
    #         )
    #     ]


class Booking(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")
    bookable_item = models.ForeignKey(
        BookableItem,
        on_delete=models.CASCADE,
        related_name="bookings",
        null=True,
        blank=True,
    )

    def clean(self):
        if (
            self.bookable_item == None
            and User.conditions["booking"]["must_have_bookable_item"] == True
        ):
            raise ValidationError("Bookable item is required")

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=["order", "event", "created_by"],
    #             name="unique_booking_for_order_and_event",
    #             condition=models.Q(
    #                 User.conditions["booking"]["dublicate_booking"] == True
    #             ),
    #             violation_error_message="Booking already attributed for this order and event",
    #         )
    #     ]
