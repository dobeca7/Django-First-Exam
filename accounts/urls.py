from django.urls import path

from accounts.views import (
    AccountLoginView,
    AccountLogoutView,
    DashboardView,
    ProfileUpdateView,
    RegisterView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="account-register"),
    path("login/", AccountLoginView.as_view(), name="account-login"),
    path("logout/", AccountLogoutView.as_view(), name="account-logout"),
    path("dashboard/", DashboardView.as_view(), name="account-dashboard"),
    path("profile/edit/", ProfileUpdateView.as_view(), name="account-profile-edit"),
]
