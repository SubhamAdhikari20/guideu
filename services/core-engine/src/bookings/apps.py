from django.apps import AppConfig


class BookingsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.bookings'
    verbose_name = 'Bookings'

    def ready(self) -> None:
        try:
            import src.bookings.signals  # noqa: F401
        except Exception:
            pass
