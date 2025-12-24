from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.services.dashboard'
    verbose_name = 'Dashboard'

    def ready(self):
        import src.services.dashboard.signals  # noqa