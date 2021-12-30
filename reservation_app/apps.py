from django.apps import AppConfig
from selenium.webdriver import Safari
import os


LIB_ADRESS = "https://www.ub.tum.de/arbeitsplatz-reservieren"


class ReservationAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reservation_app'
    driver = None

    def ready(self):
        # python manage.py runserver runs the ready method twice — once in each of two processes —
        # but we only want to run it once.
        if os.environ.get('RUN_MAIN', None) != 'true':
            # jobs.start_scheduler()
            #self.driver = Safari()
            #self.driver.get(LIB_ADRESS)
            ...
