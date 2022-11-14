from django.contrib import admin
from .models import *


class BookableLocationAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "created_by")


admin.site.register(BookableLocation)


class SeatAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "bookable_location",
        "row",
        "restricted",
        "created_by",
    )


admin.site.register(Seat)


class LocationBookingAdmin(admin.ModelAdmin):
    list_display = (
        "bookable_location",
        "start_time",
        "end_time",
        "event",
        "created_by",
    )


admin.site.register(LocationBooking)


class SeatBookingAdmin(admin.ModelAdmin):
    list_display = ("customer", "seat", "created_by")


admin.site.register(SeatBooking)
