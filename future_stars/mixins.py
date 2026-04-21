from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class AccountRequiredMixin(LoginRequiredMixin):
    login_message = "Please log in or create an account to access this section."

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, self.login_message)
        return super().handle_no_permission()


class SuperuserPermissionRequiredMixin(PermissionRequiredMixin):
    def has_permission(self):
        return self.request.user.is_superuser or super().has_permission()
