from datetime import date

from django.contrib.auth.models import Permission
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from academies.models import Academy
from accounts.models import AppUser
from players.forms import PlayerDeleteForm, PlayerForm
from players.models import Player


class PlayerAppTests(TestCase):
    def setUp(self):
        self.owner = AppUser.objects.create_user(
            username="owner",
            password="testpass123",
            role=AppUser.RoleChoices.ACADEMY_MANAGER,
        )
        self.other_user = AppUser.objects.create_user(
            username="other",
            password="testpass123",
            role=AppUser.RoleChoices.ANALYST,
        )
        self.academy = Academy.objects.create(
            owner=self.owner,
            name="Alpha Academy",
            city="Sofia",
            founded_year=2008,
            contact_email="alpha@example.com",
        )
        self.other_academy = Academy.objects.create(
            owner=self.other_user,
            name="Beta Academy",
            city="Plovdiv",
            founded_year=2009,
            contact_email="beta@example.com",
        )
        self.player = Player.objects.create(
            name="Ivan Petrov",
            birth_date=date(2005, 5, 15),
            nationality="Bulgarian",
            height=180,
            weight=75,
            position=Player.PositionChoices.MIDFIELDER,
            dominant_foot=Player.DominantFootChoices.RIGHT,
            potential=88,
            academy=self.academy,
        )

    def test_player_model_full_clean_when_birth_date_is_before_allowed_minimum_should_raise_birth_date_validation_error(self):
        player = Player(
            name="Too Old Prospect",
            birth_date=date(1999, 12, 31),
            nationality="Bulgarian",
            height=178,
            weight=70,
            position=Player.PositionChoices.DEFENDER,
            dominant_foot=Player.DominantFootChoices.LEFT,
            potential=70,
            academy=self.academy,
        )

        with self.assertRaises(ValidationError) as error:
            player.full_clean()

        self.assertIn("birth_date", error.exception.message_dict)

    def test_player_model_full_clean_when_goalkeeper_has_both_dominant_feet_should_raise_dominant_foot_validation_error(self):
        player = Player(
            name="Impossible Goalkeeper",
            birth_date=date(2006, 1, 1),
            nationality="Bulgarian",
            height=190,
            weight=80,
            position=Player.PositionChoices.GOALKEEPER,
            dominant_foot=Player.DominantFootChoices.BOTH,
            potential=79,
            academy=self.academy,
        )

        with self.assertRaises(ValidationError) as error:
            player.full_clean()

        self.assertIn("dominant_foot", error.exception.message_dict)

    def test_player_form_when_initialized_for_non_superuser_should_limit_academy_queryset_to_owned_academies_only(self):
        form = PlayerForm(user=self.owner)

        self.assertQuerySetEqual(
            form.fields["academy"].queryset.order_by("pk"),
            [self.academy],
            transform=lambda academy: academy,
        )
        self.assertNotIn("average_report_rating", form.fields)
        self.assertNotIn("report_count", form.fields)

    def test_player_form_when_height_is_over_maximum_should_be_invalid_with_expected_height_error_message(self):
        form = PlayerForm(
            data={
                "name": "Tall Prospect",
                "birth_date": "2006-04-10",
                "nationality": "Bulgarian",
                "height": 301,
                "weight": 70,
                "position": Player.PositionChoices.DEFENDER,
                "dominant_foot": Player.DominantFootChoices.RIGHT,
                "potential": 80,
                "academy": self.academy.pk,
            },
            user=self.owner,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Height must be between 1 and 300 cm.", form.errors["height"])

    def test_player_delete_form_when_rendered_for_confirmation_should_have_all_fields_disabled(self):
        form = PlayerDeleteForm(instance=self.player)

        self.assertTrue(all(field.disabled for field in form.fields.values()))

    def test_player_create_view_when_logged_in_user_has_no_owned_academies_should_return_permission_denied_response(self):
        user_without_academy = AppUser.objects.create_user(
            username="noacademy",
            password="testpass123",
            role=AppUser.RoleChoices.ANALYST,
        )
        add_permission = Permission.objects.get(codename="add_player")
        user_without_academy.user_permissions.add(add_permission)
        self.client.force_login(user_without_academy)

        response = self.client.get(reverse("player-create"))

        self.assertEqual(response.status_code, 403)

    def test_player_edit_view_when_anonymous_user_requests_page_should_redirect_to_login(self):
        response = self.client.get(reverse("player-edit", args=[self.player.pk]))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account-login"), response.url)

    def test_player_edit_view_when_authenticated_user_has_permission_but_is_not_owner_should_return_not_found(self):
        change_permission = Permission.objects.get(codename="change_player")
        self.other_user.user_permissions.add(change_permission)
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("player-edit", args=[self.player.pk]))

        self.assertEqual(response.status_code, 404)

    def test_compare_players_view_when_more_than_three_players_are_selected_should_show_exact_selection_error_message(self):
        self.client.force_login(self.owner)

        player_two = Player.objects.create(
            name="Second Player",
            birth_date=date(2006, 6, 6),
            nationality="Bulgarian",
            height=176,
            weight=68,
            position=Player.PositionChoices.DEFENDER,
            dominant_foot=Player.DominantFootChoices.LEFT,
            potential=77,
            academy=self.academy,
        )
        player_three = Player.objects.create(
            name="Third Player",
            birth_date=date(2007, 7, 7),
            nationality="Bulgarian",
            height=172,
            weight=67,
            position=Player.PositionChoices.FORWARD,
            dominant_foot=Player.DominantFootChoices.RIGHT,
            potential=82,
            academy=self.academy,
        )
        player_four = Player.objects.create(
            name="Fourth Player",
            birth_date=date(2008, 8, 8),
            nationality="Bulgarian",
            height=174,
            weight=65,
            position=Player.PositionChoices.MIDFIELDER,
            dominant_foot=Player.DominantFootChoices.RIGHT,
            potential=85,
            academy=self.academy,
        )

        response = self.client.get(
            reverse("player-compare"),
            {"players": [self.player.pk, player_two.pk, player_three.pk, player_four.pk]},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["compare_error"], "Please select exactly 2 or 3 players.")
