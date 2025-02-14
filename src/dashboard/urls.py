from django.urls import path

from dashboard.views.dashboard import DashboardTemplateView

urlpatterns = [
    path(
        '',
        DashboardTemplateView.as_view(),
    ),
]
