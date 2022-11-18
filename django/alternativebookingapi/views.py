from .serializers import *
from .models import *
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from rest_framework.response import Response
from django.db.models import F
from django.db import transaction

from django.contrib.auth.models import Group, User

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class BaseViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_superuser:
            return self.queryset.all()
        return self.queryset.filter(created_by=self.request.user)

    class Meta:
        abstract = True


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    # auto create token on user creation
    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            Token.objects.create(user=instance)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated]


class LocationViewSet(BaseViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filterset_fields = ["name"]


class BookableItemViewSet(BaseViewSet):
    queryset = BookableItem.objects.all()
    serializer_class = BookableItemSerializer
    permission_classes = [IsAuthenticated, IsOwner]


class EventViewSet(BaseViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsOwner]


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
