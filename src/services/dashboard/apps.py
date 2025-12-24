from django.apps import AppConfig


class DashboardAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'src.services.dashboard'
    verbose_name = 'Dashboard'

    def ready(self):
        import src.web.dashboard.signals  # noqa