from django.apps import AppConfig


class LocationConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "location"

    def ready(self):
        from .spatial_service import spatial_service

        spatial_service.load()
