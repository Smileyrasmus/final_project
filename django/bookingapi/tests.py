from django.test import TestCase
from accounts.models import CustomUser
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import *
from rest_framework.test import APIClient


# class SetUp(TestCase):
#     def setUp(self):
#         self.test_user = CustomUser.objects.create_user(
#             username="testuser", password="testuser"
#         )


class SetUpAPI(APITestCase):
    def setUp(self):
        test_user = CustomUser.objects.create_user(
            username="testuser", password="testuser"
        )
        self.client = APIClient()
        self.client.force_login(user=test_user)

    def tearDown(self):
        self.client.logout()
        return super().tearDown()


class BookableItemTests(SetUpAPI):
    def test_create_bookable_item(self):
        url = reverse("bookableitem-list")
        data = {"name": "Test Item", "description": "Test Description"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookableItem.objects.count(), 1)
        self.assertEqual(BookableItem.objects.get().name, "Test Item")

    def test_get_bookable_item(self):
        url = reverse("bookableitem-list")
        data = {"name": "Test Item", "description": "Test Description"}
        response = self.client.post(url, data, format="json")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(BookableItem.objects.count(), 1)
        self.assertEqual(BookableItem.objects.get().name, "Test Item")
