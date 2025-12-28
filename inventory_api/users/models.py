from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    OWNER = 'owner'
    WORKER = 'worker'

    ROLE_CHOICES = [
        (OWNER, 'Owner'),
        (WORKER, 'Worker'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=WORKER
    )

    def __str__(self):
        return f"{self.username} ({self.role})"

