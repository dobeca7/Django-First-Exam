from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm
from accounts.models import AppUser


class AppUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = AppUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "favorite_position",
            "bio",
        )
        labels = {
            "favorite_position": "Favourite position",
        }
        help_texts = {
            "username": "Use letters, digits, and @/./+/-/_ only.",
            "favorite_position": "Optional. Example: Central Midfielder.",
            "bio": "Optional short introduction up to 300 characters.",
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Choose a username"}),
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "favorite_position": forms.TextInput(attrs={"placeholder": "Example: Goalkeeper"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about your football focus..."}),
        }
        error_messages = {
            "username": {
                "unique": "This username is already taken.",
            },
            "email": {
                "invalid": "Please enter a valid email address.",
            },
        }

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"placeholder": "Create a strong password"}),
        help_text="Use at least 8 characters and avoid common passwords.",
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={"placeholder": "Repeat your password"}),
    )


class AppUserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
        error_messages={"required": "Please enter your username."},
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
        error_messages={"required": "Please enter your password."},
    )


class AppUserUpdateForm(UserChangeForm):
    password = None

    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "role",
            "favorite_position",
            "bio",
        )
        help_texts = {
            "username": "Your username cannot be changed casually, so keep it professional.",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "favorite_position": forms.TextInput(attrs={"placeholder": "Example: Right Back"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Short profile summary..."}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].help_text = "Choose a stable username for your scouting profile."


class AppUserAdminChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = AppUser
        fields = "__all__"

