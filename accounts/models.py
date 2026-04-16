from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.db.utils import OperationalError, ProgrammingError


class AppUser(AbstractUser):
    ROLE_GROUP_NAMES = {
        "academy_manager": "Academy Managers",
        "scout": "Scouts",
        "analyst": "Analysts",
    }
    GROUP_PERMISSION_CODES = {
        "Academy Managers": [
            "add_academy",
            "change_academy",
            "delete_academy",
            "view_academy",
            "add_player",
            "change_player",
            "delete_player",
            "view_player",
        ],
        "Scouts": [
            "add_scoutreport",
            "change_scoutreport",
            "delete_scoutreport",
            "view_scoutreport",
            "view_player",
            "view_academy",
        ],
        "Analysts": [
            "view_academy",
            "view_player",
            "view_scoutreport",
        ],
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
        self.sync_managed_group_permissions()
        self.sync_role_group_membership()

    def _get_managed_groups(self):
        try:
            return {
                group.name: group
                for group in Group.objects.filter(name__in=self.ROLE_GROUP_NAMES.values())
            }
        except (OperationalError, ProgrammingError):
            return {}

    def sync_managed_group_permissions(self):
        managed_groups = self._get_managed_groups()

        try:
            for group_name, permission_codes in self.GROUP_PERMISSION_CODES.items():
                group = managed_groups.get(group_name)
                if group is None:
                    group = Group.objects.create(name=group_name)
                    managed_groups[group_name] = group

                permissions = Permission.objects.filter(codename__in=permission_codes)
                group.permissions.set(permissions)
        except (OperationalError, ProgrammingError):
            return

    def sync_role_group_membership(self):
        if not self.pk or self.is_superuser:
            return

        managed_groups = self._get_managed_groups()

        if managed_groups:
            self.groups.remove(*managed_groups.values())

        target_group_name = self.ROLE_GROUP_NAMES.get(self.role)
        if not target_group_name:
            return

        target_group = managed_groups.get(target_group_name)
        if target_group is None:
            return

        self.groups.add(target_group)

    def __str__(self):
        full_name = self.get_full_name().strip()
        return full_name or self.username
