from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin


class AccountRequiredMixin(LoginRequiredMixin):
    login_message = "Please log in or create an account to access this section."

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.info(self.request, self.login_message)
        return super().handle_no_permission()
