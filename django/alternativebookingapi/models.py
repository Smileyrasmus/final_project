from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class BaseModel(models.Model):
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
    note = models.CharField(max_length=255, blank=True, null=True)


class Event(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class Booking(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="bookings")


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

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "location"],
                name="unique_item_name_for_location",
                violation_error_message="Item already attributed for this location",
            )
        ]
