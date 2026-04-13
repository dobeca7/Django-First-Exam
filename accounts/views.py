from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from accounts.forms import AppUserCreationForm, AppUserLoginForm, AppUserUpdateForm
from accounts.models import AppUser


class RegisterView(SuccessMessageMixin, CreateView):
    model = AppUser
    form_class = AppUserCreationForm
    template_name = "accounts/register.html"
    success_url = reverse_lazy("account-login")
    success_message = "Your account was created successfully. You can now log in."


class AccountLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = AppUserLoginForm
    redirect_authenticated_user = True


class AccountLogoutView(LogoutView):
    next_page = reverse_lazy("home")


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/dashboard.html"


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AppUser
    form_class = AppUserUpdateForm
    template_name = "accounts/profile-form.html"
    success_url = reverse_lazy("account-dashboard")
    success_message = "Your profile was updated successfully."

    def get_object(self, queryset=None):
        return self.request.user
