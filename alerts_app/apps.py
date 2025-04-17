from django.apps import AppConfig

class AlertsAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'alerts_app'

    def ready(self):
        import alerts_app.signals