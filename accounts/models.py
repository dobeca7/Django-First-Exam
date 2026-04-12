from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        ACADEMY_MANAGER = "academy_manager", "Academy Manager"
        SCOUT = "scout", "Scout"
        ANALYST = "analyst", "Analyst"

    role = models.CharField(
        max_length=30,
        choices=RoleChoices,
        default=RoleChoices.ANALYST,
    )
    favorite_position = models.CharField(max_length=30, blank=True)
    bio = models.TextField(max_length=300, blank=True)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username

