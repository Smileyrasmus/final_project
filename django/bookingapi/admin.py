from django.contrib import admin

from .models import Order, Event, Booking, Location, BookableItem


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "note",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


admin.site.register(Order, OrderAdmin)


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "start_time",
        "end_time",
        "created_at",
    )


admin.site.register(Event, EventAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "order",
        "event",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


admin.site.register(Booking, BookingAdmin)


class LocationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


admin.site.register(Location, LocationAdmin)


class bookableItemAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "description",
        "active",
        "location",
        "created_at",
        "updated_at",
        "created_by",
        "updated_by",
    )


admin.site.register(BookableItem, bookableItemAdmin)
