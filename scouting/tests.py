from datetime import date
from unittest.mock import patch

from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from academies.models import Academy
from accounts.models import AppUser
from players.models import Player
from scouting.choices import RecommendationChoices
from scouting.forms import ScoutReportForm
from scouting.models import ScoutReport, Skill


class ScoutingAppTests(TestCase):
    def setUp(self):
        self.owner = AppUser.objects.create_user(
            username="scout_owner",
            password="testpass123",
            role=AppUser.RoleChoices.SCOUT,
        )
        self.other_user = AppUser.objects.create_user(
            username="foreign_scout",
            password="testpass123",
            role=AppUser.RoleChoices.SCOUT,
        )
        self.superuser = AppUser.objects.create_superuser(
            username="admin",
            password="testpass123",
            email="admin@example.com",
        )
        self.academy = Academy.objects.create(
            owner=self.owner,
            name="Gamma Academy",
            city="Varna",
            founded_year=2010,
            contact_email="gamma@example.com",
        )
        self.player = Player.objects.create(
            name="Scout Target",
            birth_date=date(2006, 3, 21),
            nationality="Bulgarian",
            height=177,
            weight=69,
            position=Player.PositionChoices.FORWARD,
            dominant_foot=Player.DominantFootChoices.RIGHT,
            potential=91,
            academy=self.academy,
        )
        self.skill_b, _ = Skill.objects.get_or_create(name="Dribbling", defaults={"skill": "db"})
        self.skill_a, _ = Skill.objects.get_or_create(name="Acceleration", defaults={"skill": "ac"})
        self.report = ScoutReport.objects.create(
            owner=self.owner,
            player=self.player,
            scout_name="Lead Scout",
            rating=8,
            recommendation=RecommendationChoices.MONITOR,
            notes="Strong first impression.",
        )

    def test_scout_report_form_when_sign_recommendation_is_combined_with_rating_below_seven_should_be_invalid_with_recommendation_error(self):
        form = ScoutReportForm(
            data={
                "player": self.player.pk,
                "scout_name": "Junior Scout",
                "rating": 6,
                "recommendation": RecommendationChoices.SIGN,
                "notes": "Not ready yet.",
                "skills": [self.skill_a.pk],
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Use 'Sign' only for ratings over 7.", form.errors["recommendation"])

    def test_scout_report_form_when_initialized_should_order_available_skills_alphabetically_by_name(self):
        form = ScoutReportForm()
        skill_names = list(form.fields["skills"].queryset.values_list("name", flat=True))

        self.assertEqual(skill_names, sorted(skill_names))
        self.assertIn("Acceleration", skill_names)
        self.assertIn("Dribbling", skill_names)

    @patch("scouting.views.update_player_report_stats.delay")
    def test_scout_report_create_view_when_non_superuser_submits_valid_form_should_save_owner_and_queue_stats_task(self, mocked_delay):
        add_permission = Permission.objects.get(codename="add_scoutreport")
        self.owner.user_permissions.add(add_permission)
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("report-create"),
            data={
                "player": self.player.pk,
                "scout_name": "Match Observer",
                "rating": 9,
                "recommendation": RecommendationChoices.SIGN,
                "notes": "Immediate impact.",
                "skills": [self.skill_a.pk, self.skill_b.pk],
            },
        )

        created_report = ScoutReport.objects.exclude(pk=self.report.pk).get()
        self.assertRedirects(response, reverse("report-list"))
        self.assertEqual(created_report.owner, self.owner)
        mocked_delay.assert_called_once_with(self.player.pk)

    def test_scout_report_edit_view_when_authenticated_user_has_permission_but_does_not_own_report_should_return_not_found(self):
        change_permission = Permission.objects.get(codename="change_scoutreport")
        self.other_user.user_permissions.add(change_permission)
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("report-edit", args=[self.report.pk]))

        self.assertEqual(response.status_code, 404)

    def test_scout_report_delete_view_when_authenticated_user_has_permission_but_does_not_own_report_should_return_not_found(self):
        delete_permission = Permission.objects.get(codename="delete_scoutreport")
        self.other_user.user_permissions.add(delete_permission)
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("report-delete", args=[self.report.pk]))

        self.assertEqual(response.status_code, 404)

    @patch("scouting.views.update_player_report_stats.delay")
    def test_scout_report_edit_view_when_owner_submits_valid_update_should_queue_stats_recalculation_for_same_player(self, mocked_delay):
        change_permission = Permission.objects.get(codename="change_scoutreport")
        self.owner.user_permissions.add(change_permission)
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("report-edit", args=[self.report.pk]),
            data={
                "player": self.player.pk,
                "scout_name": "Lead Scout Updated",
                "rating": 9,
                "recommendation": RecommendationChoices.SIGN,
                "notes": "Now clearly ready.",
                "skills": [self.skill_a.pk],
            },
        )

        self.assertRedirects(response, reverse("report-list"))
        mocked_delay.assert_called_once_with(self.player.pk)

    @patch("scouting.views.update_player_report_stats.delay")
    def test_scout_report_delete_view_when_owner_confirms_delete_should_remove_report_and_queue_stats_recalculation(self, mocked_delay):
        delete_permission = Permission.objects.get(codename="delete_scoutreport")
        self.owner.user_permissions.add(delete_permission)
        self.client.force_login(self.owner)

        response = self.client.post(reverse("report-delete", args=[self.report.pk]))

        self.assertRedirects(response, reverse("report-list"))
        self.assertFalse(ScoutReport.objects.filter(pk=self.report.pk).exists())
        mocked_delay.assert_called_once_with(self.player.pk)
