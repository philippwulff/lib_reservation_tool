from django.core.management import BaseCommand
from .common.exceptions import WebpageLocatorError
from .common.page import LandingPage, BookingPage


class Command(BaseCommand):
    def handle(self, *args, **options):
        while True:
            ...