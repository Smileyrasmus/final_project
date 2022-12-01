from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from django.db.models import F
from django.db import transaction
from rest_framework.decorators import action

from django.contrib.auth.models import Group, User


class BaseReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(created_by=self.request.user)

    class Meta:
        abstract = True


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(created_by=self.request.user)

    class Meta:
        abstract = True


class LocationViewSet(BaseViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ["name"]


class BookableItemViewSet(BaseViewSet):
    queryset = BookableItem.objects.all()
    serializer_class = BookableItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ["name", "location"]

    def create(self, request, *args, **kwargs):
        """
        #checks if post request data is an array initializes serializer with many=True
        else executes default CreateModelMixin.create function
        """
        is_many = isinstance(request.data, list)
        if not is_many:
            return super(BookableItemViewSet, self).create(request, *args, **kwargs)
        else:
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )


class EventViewSet(BaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ["name", "start_time", "end_time"]


class BookingViewSet(BaseReadOnlyViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ["event"]

    @action(detail=False, url_path="bookable-items")
    def get_bookable_items_only(self, request):
        if not request.query_params.get("event"):
            return Response(
                {"event": "This field is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        bookable_items = self.filter_queryset(self.queryset).values("bookable_item")
        # make to a list of strings instead of list of objects
        bookable_items_ids = map(lambda b: b["bookable_item"], bookable_items)
        return Response(bookable_items_ids)


class OrderViewSet(BaseViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        if not request.data.get("bookings"):
            return Response(
                {"bookings": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data["order"])
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        for booking in request.data["bookings"]:
            booking["order"] = instance.id
            self.serializer_class = BookingSerializer
            booking_serializer = self.get_serializer(data=booking)
            booking_serializer.is_valid(raise_exception=True)
            booking_serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
