from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.utils import OperationalError, ProgrammingError


class AppUser(AbstractUser):
    ROLE_GROUP_NAMES = {
        "academy_manager": "Academy Managers",
        "scout": "Scouts",
        "analyst": "Analysts",
    }

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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.sync_role_group_membership()

    def sync_role_group_membership(self):
        if not self.pk or self.is_superuser:
            return

        try:
            managed_groups = list(Group.objects.filter(name__in=self.ROLE_GROUP_NAMES.values()))
        except (OperationalError, ProgrammingError):
            return

        if managed_groups:
            self.groups.remove(*managed_groups)

        target_group_name = self.ROLE_GROUP_NAMES.get(self.role)
        if not target_group_name:
            return

        try:
            target_group = Group.objects.get(name=target_group_name)
        except Group.DoesNotExist:
            return

        self.groups.add(target_group)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username
