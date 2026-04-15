from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from academies.models import Academy
from players.models import Player
from scouting.models import ScoutReport


UserModel = get_user_model()


class RolePermissionTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.academy = Academy.objects.create(
            name="Blue Talents",
            city="Sofia",
            founded_year=2010,
            contact_email="academy@example.com",
        )
        cls.player = Player.objects.create(
            name="Ivan Petrov",
            birth_date=date(2008, 5, 10),
            nationality="Bulgarian",
            height=180,
            weight=72,
            position=Player.PositionChoices.MIDFIELDER,
            dominant_foot=Player.DominantFootChoices.RIGHT,
            potential=91,
            academy=cls.academy,
        )
        cls.report = ScoutReport.objects.create(
            player=cls.player,
            scout_name="Senior Scout",
            rating=8,
            recommendation="sign",
            notes="Strong transitional play.",
        )

    def create_user(self, username, role):
        return UserModel.objects.create_user(
            username=username,
            password="testpass123",
            role=role,
        )

    def test_scout_is_assigned_only_to_scout_group(self):
        scout = self.create_user("scout_user", UserModel.RoleChoices.SCOUT)

        self.assertQuerySetEqual(
            scout.groups.order_by("name").values_list("name", flat=True),
            ["Scouts"],
            transform=lambda value: value,
        )
        self.assertTrue(scout.has_perm("scouting.add_scoutreport"))
        self.assertFalse(scout.has_perm("players.add_player"))
        self.assertFalse(scout.has_perm("academies.add_academy"))

    def test_academy_manager_is_assigned_only_to_manager_group(self):
        manager = self.create_user("manager_user", UserModel.RoleChoices.ACADEMY_MANAGER)

        self.assertQuerySetEqual(
            manager.groups.order_by("name").values_list("name", flat=True),
            ["Academy Managers"],
            transform=lambda value: value,
        )
        self.assertTrue(manager.has_perm("players.add_player"))
        self.assertTrue(manager.has_perm("academies.add_academy"))
        self.assertFalse(manager.has_perm("scouting.add_scoutreport"))

    def test_analyst_is_assigned_only_to_read_only_group(self):
        analyst = self.create_user("analyst_user", UserModel.RoleChoices.ANALYST)

        self.assertQuerySetEqual(
            analyst.groups.order_by("name").values_list("name", flat=True),
            ["Analysts"],
            transform=lambda value: value,
        )
        self.assertTrue(analyst.has_perm("players.view_player"))
        self.assertTrue(analyst.has_perm("academies.view_academy"))
        self.assertTrue(analyst.has_perm("scouting.view_scoutreport"))
        self.assertFalse(analyst.has_perm("players.add_player"))
        self.assertFalse(analyst.has_perm("academies.add_academy"))
        self.assertFalse(analyst.has_perm("scouting.add_scoutreport"))

    def test_changing_role_reassigns_managed_group(self):
        user = self.create_user("switch_user", UserModel.RoleChoices.SCOUT)

        user.role = UserModel.RoleChoices.ACADEMY_MANAGER
        user.save()

        self.assertQuerySetEqual(
            user.groups.order_by("name").values_list("name", flat=True),
            ["Academy Managers"],
            transform=lambda value: value,
        )

    def test_scout_can_access_only_report_crud_entry_points(self):
        scout = self.create_user("scout_access", UserModel.RoleChoices.SCOUT)
        self.client.force_login(scout)

        self.assertEqual(self.client.get(reverse("report-create")).status_code, 200)
        self.assertEqual(self.client.get(reverse("report-edit", args=[self.report.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("report-delete", args=[self.report.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("player-create")).status_code, 403)
        self.assertEqual(self.client.get(reverse("academy-create")).status_code, 403)

    def test_academy_manager_can_access_player_and_academy_crud_only(self):
        manager = self.create_user("manager_access", UserModel.RoleChoices.ACADEMY_MANAGER)
        self.client.force_login(manager)

        self.assertEqual(self.client.get(reverse("player-create")).status_code, 200)
        self.assertEqual(self.client.get(reverse("player-edit", args=[self.player.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("player-delete", args=[self.player.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("academy-create")).status_code, 200)
        self.assertEqual(self.client.get(reverse("academy-edit", args=[self.academy.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("academy-delete", args=[self.academy.pk])).status_code, 200)
        self.assertEqual(self.client.get(reverse("report-create")).status_code, 403)

    def test_analyst_cannot_access_any_crud_entry_point(self):
        analyst = self.create_user("analyst_access", UserModel.RoleChoices.ANALYST)
        self.client.force_login(analyst)

        self.assertEqual(self.client.get(reverse("player-create")).status_code, 403)
        self.assertEqual(self.client.get(reverse("academy-create")).status_code, 403)
        self.assertEqual(self.client.get(reverse("report-create")).status_code, 403)
