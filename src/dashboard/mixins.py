from django.contrib.auth.mixins import LoginRequiredMixin

class AuthMixin(LoginRequiredMixin):
    login_url = "/login/"
