from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


class basemodel(models.Model):
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


class BookableLocation(basemodel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.created_by

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "created_by"],
                name="unique_location_name",
                violation_error_message="You already have a location with this name",
            )
        ]


class Seat(basemodel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    bookable_location = models.ForeignKey(
        BookableLocation, on_delete=models.CASCADE, related_name="seats"
    )
    restricted = models.BooleanField(default=False)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.created_by

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "bookable_location"],
                name="unique_seat_name",
                violation_error_message="You already have a seat with this name",
            )
        ]


class LocationBooking(basemodel):
    bookable_location = models.ForeignKey(
        "BookableLocation", on_delete=models.CASCADE, related_name="location_bookings"
    )
    event_name = models.CharField(max_length=255)
    event_description = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.created_by

    def save(self, *args, **kwargs):
        if self.start_time >= self.end_time:
            raise ValidationError("Start time must be before end time")
        if self.id is None:
            if LocationBooking.objects.filter(
                bookable_location=self.bookable_location,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time,
            ).exists():
                raise ValidationError("Location already booked for this time")
        else:
            if (
                LocationBooking.objects.filter(
                    bookable_location=self.bookable_location,
                    start_time__lt=self.end_time,
                    end_time__gt=self.start_time,
                )
                .exclude(id=self.id)
                .exists()
            ):
                raise ValidationError("Location already booked for this time")
        super().save(*args, **kwargs)


class SeatBooking(basemodel):
    customer = models.CharField(max_length=255)
    seat = models.ForeignKey(
        "Seat", on_delete=models.CASCADE, related_name="seat_bookings"
    )
    location_booking = models.ForeignKey(
        "LocationBooking", on_delete=models.CASCADE, related_name="seat_bookings"
    )

    @staticmethod
    def has_read_permission(request):
        return True

    def has_object_read_permission(self, request):
        return True

    @staticmethod
    def has_write_permission(request):
        return True

    def has_object_write_permission(self, request):
        return request.user == self.created_by
