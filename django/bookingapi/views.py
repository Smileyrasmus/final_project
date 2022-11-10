from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from bookingapi.serializers import UserSerializer, GroupSerializer, BookableLocationSerializer, SeatSerializer, LocationBookingSerializer, SeatBookingSerializer, EventSerializer
from bookingapi.models import BookableLocation, Seat, LocationBooking, SeatBooking, Event
from rest_framework.permissions import IsAuthenticated
from dry_rest_permissions.generics import DRYPermissions

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
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
        return super().get_queryset().filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)

class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows events to be viewed or edited.
    """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (DRYPermissions,)
    
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)
    
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
        return super().get_queryset().filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)
    
class LocationBookingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows location bookings to be viewed or edited.
    """
    queryset = LocationBooking.objects.all()
    serializer_class = LocationBookingSerializer
    permission_classes = (DRYPermissions,)
    
    def get_queryset(self):
        return super().get_queryset().filter(created_by=self.request.user)
    
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
        return super().get_queryset().filter(created_by=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save(updated=self.request.user)