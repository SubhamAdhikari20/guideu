from django.apps import AppConfig


class PermitsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.permits'
    verbose_name = 'Permits'

    def ready(self) -> None:
        try:
            import src.permits.signals  # noqa: F401
        except Exception:
            pass
