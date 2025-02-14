from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^social/', include('social_django.urls', namespace='social')),
    re_path(r'^auth/', include('drf_social_oauth2.urls', namespace='drf')),
    path(
        'login/',
        TemplateView.as_view(
            template_name='auth/login.html',
            content_type='text/html',
        ),
    ),
    path('dashboard/', include('dashboard.urls')),
    path('transaction/', include('transaction.urls')),
]
