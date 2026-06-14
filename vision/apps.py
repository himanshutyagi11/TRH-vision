from django.apps import AppConfig
import os
import sys

class VisionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vision'

    def ready(self):
        is_runserver = 'runserver' in sys.argv
        if not is_runserver or os.environ.get('RUN_MAIN') == 'true':
            from .views import start_approved_enrollments_dispatcher
            start_approved_enrollments_dispatcher()
