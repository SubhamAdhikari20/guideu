from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.payments'
    verbose_name = 'Payments'

    def ready(self) -> None:
        try:
            import src.payments.signals  # noqa: F401
        except Exception:
            pass
