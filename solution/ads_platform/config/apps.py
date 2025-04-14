import sys

from django.apps import AppConfig


class ConfigConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'config'

    def create_false_var(self, key: str):
        try:
            from .models import Config

            Config.objects.create(
                key=key,
                value=0
            )
        except Exception:
            ...

    def ready(self):
        if 'runserver' not in sys.argv:
            return True
        
        self.create_false_var("current_time")
        self.create_false_var("moderation_enabled")
