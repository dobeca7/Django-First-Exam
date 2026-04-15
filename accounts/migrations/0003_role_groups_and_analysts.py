from django.db import migrations


ROLE_GROUP_NAMES = {
    "academy_manager": "Academy Managers",
    "scout": "Scouts",
    "analyst": "Analysts",
}


def sync_groups_and_permissions(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    AppUser = apps.get_model("accounts", "AppUser")

    group_permissions = {
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

    groups = {}
    for group_name, permission_codes in group_permissions.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=permission_codes)
        group.permissions.set(permissions)
        groups[group_name] = group

    managed_group_names = list(group_permissions.keys())
    managed_groups = Group.objects.filter(name__in=managed_group_names)

    for user in AppUser.objects.all():
        if user.is_superuser:
            continue

        user.groups.remove(*managed_groups)
        target_group_name = ROLE_GROUP_NAMES.get(user.role)
        if target_group_name:
            user.groups.add(groups[target_group_name])


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Academy Managers", "Scouts", "Analysts"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_groups_and_permissions"),
    ]

    operations = [
        migrations.RunPython(sync_groups_and_permissions, remove_groups),
    ]
