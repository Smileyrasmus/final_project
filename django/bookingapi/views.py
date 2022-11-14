from bookingapi.models import *
from bookingapi.serializers import *
from dry_rest_permissions.generics import DRYPermissions
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.core.exceptions import ValidationError
from django.db.models import Count, F

from django.contrib.auth.models import Group, User


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class BookableLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bookable locations to be viewed or edited.
    """

    queryset = BookableLocation.objects.all()
    serializer_class = BookableLocationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_superuser:
            return BookableLocation.objects.all().annotate(seat_amount=Count("seats"))
        else:
            return BookableLocation.objects.filter(
                created_by__groups__in=self.request.user.groups.all()
            ).annotate(seat_amount=Count("seats"))

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)


class SeatViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seats to be viewed or edited.
    """

    queryset = Seat.objects.all()
    serializer_class = SeatSerializer
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return Seat.objects.all()
        else:
            return Seat.objects.filter(
                created_by__groups__in=self.request.user.groups.all()
            )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)


class LocationBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows location bookings to be viewed or edited.
    """

    serializer_class = LocationBookingSerializer
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return LocationBooking.objects.all()
        else:
            return LocationBooking.objects.filter(
                created_by__groups__in=self.request.user.groups.all()
            )

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)


class SeatBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows seat bookings to be viewed or edited.
    """

    queryset = SeatBooking.objects.all()
    serializer_class = SeatBookingSerializer
    permission_classes = (DRYPermissions,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return SeatBooking.objects.all().annotate(
                seat_name=F("seat__name"),
                location_name=F("location_booking__bookable_location__name"),
                event_name=F("location_booking__event_name"),
                event_description=F("location_booking__event_description"),
                start_time=F("location_booking__start_time"),
                end_time=F("location_booking__end_time"),
            )
        else:
            return SeatBooking.objects.filter(
                created_by__groups__in=self.request.user.groups.all()
            ).annotate(
                seat_name=F("seat__name"),
                location_name=F("location_booking__bookable_location__name"),
                event_name=F("location_booking__event_name"),
                event_description=F("location_booking__event_description"),
                start_time=F("location_booking__start_time"),
                end_time=F("location_booking__end_time"),
            )

    def perform_create(self, serializer):
        if serializer.validated_data["seat"].restricted:
            raise ValidationError("Seat is restricted")
        if (
            serializer.validated_data["seat"].bookable_location
            != serializer.validated_data["location_booking"].bookable_location
        ):
            raise ValidationError(
                "Seat and location booking are not in the same location"
            )
        serializer.save(created_by=self.request.user)

    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)
