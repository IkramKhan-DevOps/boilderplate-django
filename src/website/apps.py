from django.apps import AppConfig


class WebsiteConfig(AppConfig):
    name = 'src.website'
    verbose_name = "Website"
    verbose_plural = 'Website'
    default_auto_config = 'django.db.models.BigAutoField'

    def ready(self):
        import src.core.signals  # noqa
