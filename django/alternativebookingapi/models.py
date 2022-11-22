from django.conf import settings
from django.db import models
import uuid


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


class Event(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()


class Location(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    events = models.ManyToManyField("Event", related_name="locations", blank=True)


class BookableItem(BaseModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, related_name="seats", null=True, blank=True
    )


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
