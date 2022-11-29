from django.db import models

from django.contrib.auth.models import AbstractUser
import uuid


def default_conditions():
    return dict(
        order=dict(require_customer=True),
        booking=dict(duplicate_booking=True, require_bookable_item=False),
        event=dict(start_end_overlay=True, duplicate_event=True),
        location=dict(duplicate_location=True),
        bookable_item=dict(duplicate_bookable_item=True),
    )


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conditions = models.JSONField(
        db_index=True,
        default=default_conditions,
    )
