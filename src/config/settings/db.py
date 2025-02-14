from .env import settings

DATABASES = {
    "default": {
        "ENGINE": settings.db.ENGINE,
        "NAME": settings.db.DB_NAME,
        "USER": settings.db.DB_USER,
        "PASSWORD": settings.db.DB_PASSWORD,
        "HOST": settings.db.DB_HOST,
        "PORT": settings.db.DB_PORT,
    }
}
