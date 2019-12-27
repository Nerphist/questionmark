from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    name = 'analytics'

    def ready(self):
        from .scheduler import AnalyticsScheduler
        AnalyticsScheduler.start_deleting()
