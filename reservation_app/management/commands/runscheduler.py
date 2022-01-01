from django.core.management import BaseCommand
from .common.app import App


class Command(BaseCommand):
    def handle(self, *args, **options):
        app = App("https://www.ub.tum.de/arbeitsplatz-reservieren")

        while True:
            app.refresh(sleep=3)

        app.teardown()