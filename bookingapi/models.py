from django.db import models
from django.conf import settings


class BookableLocation(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
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
        models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_per_user', violation_error_message='You already have a location with this name')
    
class Seat(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    row = models.ForeignKey("Row", on_delete=models.CASCADE, related_name="seats")
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
        models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_per_user', violation_error_message='You already have a seat with this name')
    
class Section(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    bookable_location = models.ForeignKey("BookableLocation", on_delete=models.CASCADE, related_name="sections")
    
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
        models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_per_user', violation_error_message='You already have a section with this name')
    
class Row(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, blank=True, null=True)
    section = models.ForeignKey("Section", on_delete=models.CASCADE, related_name="rows")
    
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
        models.UniqueConstraint(fields=['name', 'created_by'], name='unique_name_per_user', violation_error_message='You already have a row with this name')
    
class LocationBooking(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    bookable_location = models.ForeignKey("BookableLocation", on_delete=models.CASCADE, related_name="location_bookings")
    event = models.CharField(max_length=255)
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
            raise models.ValidationError('Start time must be before end time')

class SeatBooking(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    customer = models.CharField(max_length=255)
    seat = models.ForeignKey("Seat", on_delete=models.CASCADE, related_name="seat_bookings")
    
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
    