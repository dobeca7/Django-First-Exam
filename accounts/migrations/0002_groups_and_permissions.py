from django.db import migrations


def create_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    academy_manager_group, _ = Group.objects.get_or_create(name="Academy Managers")
    scout_group, _ = Group.objects.get_or_create(name="Scouts")

    academy_permission_codes = [
        "add_academy",
        "change_academy",
        "delete_academy",
        "view_academy",
        "add_player",
        "change_player",
        "delete_player",
        "view_player",
    ]
    scout_permission_codes = [
        "add_scoutreport",
        "change_scoutreport",
        "delete_scoutreport",
        "view_scoutreport",
        "view_player",
    ]

    academy_permissions = Permission.objects.filter(codename__in=academy_permission_codes)
    scout_permissions = Permission.objects.filter(codename__in=scout_permission_codes)

    academy_manager_group.permissions.set(academy_permissions)
    scout_group.permissions.set(scout_permissions)


def remove_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=["Academy Managers", "Scouts"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
        ("academies", "0004_alter_academy_founded_year"),
        ("players", "0003_remove_player_age_remove_player_skills_and_more"),
        ("scouting", "0004_skill_updates"),
    ]

    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]
