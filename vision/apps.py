from django.apps import AppConfig
import os
import sys

class VisionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'vision'

    def ready(self):
        # NOTE: Auto-dispatcher disabled — admin now uses the manual one-click
        # "Send Offer Letter" → "Send Credentials" flow in the enrollments panel.
        # To re-enable, uncomment the block below.
        # is_runserver = 'runserver' in sys.argv
        # if not is_runserver or os.environ.get('RUN_MAIN') == 'true':
        #     from .views import start_approved_enrollments_dispatcher
        #     start_approved_enrollments_dispatcher()
        pass
