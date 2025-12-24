from django.apps import AppConfig


class ManagementConfig(AppConfig):
    name = 'src.services.management'
    verbose_name = 'Management'
    verbose_plural = 'Management'
    default_auto_config = 'django.db.models.BigAutoField'

    def ready(self):
        import src.core.signals # noqa: F401
