from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.notifications"
    verbose_name = "Notifications"

    def ready(self) -> None:
        try:
            import src.notifications.signals  # noqa: F401
        except Exception:
            pass
