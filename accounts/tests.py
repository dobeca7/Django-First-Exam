from django.test import TestCase
from django.urls import reverse

from accounts.forms import AppUserCreationForm, AppUserLoginForm, AppUserUpdateForm
from accounts.models import AppUser


class AccountsAppTests(TestCase):
    def setUp(self):
        self.user = AppUser.objects.create_user(
            username="regularuser",
            password="testpass123",
            email="regular@example.com",
            role=AppUser.RoleChoices.SCOUT,
        )

    def test_app_user_creation_form_when_submitted_with_valid_data_should_create_user_and_keep_selected_role(self):
        form = AppUserCreationForm(
            data={
                "username": "newuser",
                "first_name": "New",
                "last_name": "User",
                "email": "newuser@example.com",
                "role": AppUser.RoleChoices.ACADEMY_MANAGER,
                "favorite_position": "Midfielder",
                "bio": "Short profile bio",
                "password1": "strongpass123",
                "password2": "strongpass123",
            }
        )

        self.assertTrue(form.is_valid(), form.errors)
        created_user = form.save()
        self.assertEqual(created_user.role, AppUser.RoleChoices.ACADEMY_MANAGER)

    def test_account_login_form_when_username_and_password_are_missing_should_return_expected_required_field_messages(self):
        form = AppUserLoginForm(data={})

        self.assertFalse(form.is_valid())
        self.assertIn("Please enter your username.", form.errors["username"])
        self.assertIn("Please enter your password.", form.errors["password"])

    def test_dashboard_view_when_anonymous_user_requests_page_should_redirect_to_login_page(self):
        response = self.client.get(reverse("account-dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("account-login"), response.url)

    def test_profile_update_view_when_authenticated_user_submits_valid_data_should_update_current_user_profile_successfully(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("account-profile-edit"),
            data={
                "username": "regularuser",
                "first_name": "Updated",
                "last_name": "Scout",
                "email": "updated@example.com",
                "role": AppUser.RoleChoices.ANALYST,
                "favorite_position": "Winger",
                "bio": "Updated bio",
            },
        )

        self.user.refresh_from_db()
        self.assertRedirects(response, reverse("account-dashboard"))
        self.assertEqual(self.user.first_name, "Updated")
        self.assertEqual(self.user.role, AppUser.RoleChoices.ANALYST)

    def test_app_user_update_form_when_initialized_for_existing_user_should_hide_password_field_and_keep_custom_username_help_text(self):
        form = AppUserUpdateForm(instance=self.user)

        self.assertNotIn("password", form.fields)
        self.assertEqual(
            form.fields["username"].help_text,
            "Choose a stable username for your scouting profile.",
        )
