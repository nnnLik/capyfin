from django.views.generic import TemplateView

from dashboard.mixins import AuthMixin


class BaseTemplateView(AuthMixin, TemplateView):
    ...
