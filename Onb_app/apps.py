from django.apps import AppConfig


class OnbAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Onb_app'

    def ready(self):
        import Onb_app.signals