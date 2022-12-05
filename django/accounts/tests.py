from django.test import TestCase
from .models import *


class SetUp(TestCase):
    def setUp(self):
        self.test_user = CustomUser.objects.create_user(
            username="testuser", password="testuser"
        )


class ConditionTests(SetUp):
    def test_change_bookable_item_duplicate(self):
        """Switch boolean for bookable item should be unique"""
        prev = self.test_user.conditions["bookable_item"]["duplicate_bookable_item"]
        self.test_user.conditions["bookable_item"]["duplicate_bookable_item"] = not prev
        self.test_user.save()
        assert (
            self.test_user.conditions["bookable_item"]["duplicate_bookable_item"]
            != prev
        )
