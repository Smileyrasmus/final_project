from django.db import models

from django.contrib.auth.models import AbstractUser
import uuid


def default_conditions():
    return dict(
        order=dict(must_have_customer_id=True),
        booking=dict(dublicate_booking=True, must_have_bookable_item=False),
        event=dict(start_end_overlay=True, dublicate_event=True),
        location=dict(dublicate_location=True),
        bookable_item=dict(dublicate_bookable_item=True, active=True),
    )


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # add additional fields in here
    conditions = models.JSONField(
        db_index=True,
        default=default_conditions,
    )
