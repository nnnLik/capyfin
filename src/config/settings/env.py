from pydantic import Field
from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    SECRET_KEY: str = Field('123waewdqdpk)(UE)(@Y(HDihadiansdo9*UY()Q')
    DEBUG: bool = Field(True)
    ALLOWED_HOSTS: list[str] = Field(['*'])
    CORS_ALLOWED_ORIGINS: list[str] = Field(['http://localhost:8012'])
    CSRF_TRUSTED_ORIGINS: list[str] = Field(['http://localhost:8012'])
    CORS_ALLOW_CREDENTIALS: bool = Field(True)
    TIME_ZONE: str = Field('UTC')

    TG_APP_TOKEN: str = Field('')
    FREE_CURRENCY_API_TOKEN: str = Field('')

    @property
    def CORS_ALLOW_ALL_ORIGINS(self) -> bool:
        return True if self.DEBUG else False


class DatabaseSettings(BaseSettings):
    ENGINE: str = Field(default='django.db.backends.postgresql')
    DB_NAME: str = Field(default='capyfin_db')
    DB_USER: str = Field(default='capyfin_user')
    DB_PASSWORD: str = Field(default='capyfin_pass')
    DB_HOST: str = Field(default='capyfin-postgres')
    DB_PORT: int = Field(default=5432)


class Settings(BaseSettings):
    app: ApplicationSettings = ApplicationSettings()
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()
