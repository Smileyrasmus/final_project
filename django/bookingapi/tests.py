from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from .models import *

class BookableLocationTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='testuser')
        BookableLocation.objects.create(name="Test Location", description="Test Description", created_by=test_user)

    def test_bookable_location(self):
        """Bookable locations should have a name and description"""
        test_location = BookableLocation.objects.get(name="Test Location")
        self.assertEqual(test_location.name, "Test Location")
        self.assertEqual(test_location.description, "Test Description")
        self.assertEqual(test_location.created_by.username, "testuser")

class SeatTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='testuser')
        test_location = BookableLocation.objects.create(name="Test Location", description="Test Description", created_by=test_user)
        Seat.objects.create(name="Test Seat", description="Test Description", bookable_location=test_location, created_by=test_user)

    def test_seat(self):
        """Seats should have a name, description and bookable location"""
        test_seat = Seat.objects.get(name="Test Seat")
        self.assertEqual(test_seat.name, "Test Seat")
        self.assertEqual(test_seat.description, "Test Description")
        self.assertEqual(test_seat.bookable_location.name, "Test Location")
        self.assertEqual(test_seat.created_by.username, "testuser")

class LocationBookingTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='testuser')
        test_location = BookableLocation.objects.create(name="Test Location", description="Test Description", created_by=test_user)
        global initial_start_time
        global initial_end_time
        initial_start_time = timezone.now()
        initial_end_time = timezone.now() + timezone.timedelta(hours=1)
        
        LocationBooking.objects.create(bookable_location=test_location, start_time=initial_start_time, end_time=initial_end_time, event_name="Test Event", event_description="Test Description", created_by=test_user)

    def test_location_booking(self):
        """Location bookings should have a bookable location, start time, end time, event name and description"""
        test_location_booking = LocationBooking.objects.get(event_name="Test Event")
        self.assertEqual(test_location_booking.bookable_location.name, "Test Location")
        self.assertEqual(test_location_booking.start_time, initial_start_time)
        self.assertEqual(test_location_booking.end_time, initial_end_time)
        self.assertEqual(test_location_booking.event_name, "Test Event")
        self.assertEqual(test_location_booking.event_description, "Test Description")
        self.assertEqual(test_location_booking.created_by.username, "testuser")

class SeatBookingTestCase(TestCase):
    def setUp(self):
        test_user = User.objects.create_user(username='testuser', password='testuser')
        test_location = BookableLocation.objects.create(name="Test Location", description="Test Description", created_by=test_user)
        test_seat = Seat.objects.create(name="Test Seat", description="Test Description", bookable_location=test_location, created_by=test_user)
        
        test_location_booking = LocationBooking.objects.create(bookable_location=test_location, start_time=initial_start_time, end_time=initial_end_time, event_name="Test Event", event_description="Test Description", created_by=test_user)
        SeatBooking.objects.create(customer="Test Customer", seat=test_seat, location_booking=test_location_booking, created_by=test_user)

    def test_seat_booking(self):
        """Seat bookings should have a customer, seat and location booking"""
        test_seat_booking = SeatBooking.objects.get(customer="Test Customer")
        self.assertEqual(test_seat_booking.customer, "Test Customer")
        self.assertEqual(test_seat_booking.seat.name, "Test Seat")
        self.assertEqual(test_seat_booking.location_booking.event_name, "Test Event")
        self.assertEqual(test_seat_booking.created_by.username, "testuser")