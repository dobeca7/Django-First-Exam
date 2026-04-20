from django.contrib.auth.models import Permission
from django.test import TestCase
from django.urls import reverse

from academies.forms import AcademyDeleteForm, AcademyForm
from academies.models import Academy
from accounts.models import AppUser


class AcademiesAppTests(TestCase):
    def setUp(self):
        self.owner = AppUser.objects.create_user(
            username="academyowner",
            password="testpass123",
            role=AppUser.RoleChoices.ACADEMY_MANAGER,
        )
        self.other_user = AppUser.objects.create_user(
            username="foreignmanager",
            password="testpass123",
            role=AppUser.RoleChoices.ACADEMY_MANAGER,
        )
        self.academy = Academy.objects.create(
            owner=self.owner,
            name="Owner Academy",
            city="Sofia",
            founded_year=2011,
            contact_email="owneracademy@example.com",
        )

    def test_academy_form_when_founded_year_is_in_the_future_should_be_invalid_with_expected_error_message(self):
        form = AcademyForm(
            data={
                "name": "Future Academy",
                "city": "Varna",
                "founded_year": 3000,
                "contact_email": "future@example.com",
            }
        )

        self.assertFalse(form.is_valid())
        self.assertIn("Use a value between 1800 and", form.errors["founded_year"][0])

    def test_academy_delete_form_when_initialized_for_confirmation_should_have_all_fields_disabled(self):
        form = AcademyDeleteForm(instance=self.academy)

        self.assertTrue(all(field.disabled for field in form.fields.values()))

    def test_academy_create_view_when_authenticated_user_has_permission_should_save_owner_as_current_user(self):
        add_permission = Permission.objects.get(codename="add_academy")
        self.owner.user_permissions.add(add_permission)
        self.client.force_login(self.owner)

        response = self.client.post(
            reverse("academy-create"),
            data={
                "name": "Created Academy",
                "city": "Burgas",
                "founded_year": 2012,
                "contact_email": "created@example.com",
            },
        )

        created_academy = Academy.objects.get(name="Created Academy")
        self.assertRedirects(response, reverse("academy-detail-slug", kwargs={"slug": created_academy.slug}))
        self.assertEqual(created_academy.owner, self.owner)

    def test_academy_edit_view_when_authenticated_user_has_permission_but_is_not_owner_should_return_not_found(self):
        change_permission = Permission.objects.get(codename="change_academy")
        self.other_user.user_permissions.add(change_permission)
        self.client.force_login(self.other_user)

        response = self.client.get(reverse("academy-edit", args=[self.academy.pk]))

        self.assertEqual(response.status_code, 404)

    def test_academy_detail_view_when_accessed_by_slug_should_return_success_and_correct_academy_in_context(self):
        self.client.force_login(self.owner)

        response = self.client.get(reverse("academy-detail-slug", kwargs={"slug": self.academy.slug}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["academy"], self.academy)
