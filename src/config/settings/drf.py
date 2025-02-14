from .env import settings

SECRET_KEY = settings.app.SECRET_KEY
ALLOWED_HOSTS = settings.app.ALLOWED_HOSTS
SECURE_CROSS_ORIGIN_OPENER_POLICY = 'same-origin-allow-popups'
SOCIAL_AUTH_TELEGRAM_BOT_TOKEN = settings.app.TG_APP_TOKEN

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOW_CREDENTIALS = settings.app.CORS_ALLOW_CREDENTIALS
CSRF_TRUSTED_ORIGINS = settings.app.CSRF_TRUSTED_ORIGINS
CORS_ALLOWED_ORIGINS = settings.app.CORS_ALLOWED_ORIGINS
CORS_ALLOW_ALL_ORIGINS = settings.app.CORS_ALLOW_ALL_ORIGINS

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'drf_social_oauth2.authentication.SocialAuthentication',
    ],
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.telegram.TelegramAuth',
    'drf_social_oauth2.backends.DjangoOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
