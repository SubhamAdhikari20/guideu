from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.authentication'
    verbose_name = 'Authentication and Accounts'

    def ready(self) -> None:
        try:
            import src.authentication.signals  # noqa: F401
        except Exception:
            pass
