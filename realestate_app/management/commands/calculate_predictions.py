import os
import django
from django.core.management.base import BaseCommand

from realestate_app.models import RealEstateListing
from realestate_app.services.price_prediction import get_listings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


class Command(BaseCommand):
    help = "Calculate price predictions and store them in database"

    def handle(self, *args, **options):
        get_listings()
        self.stdout.write(self.style.SUCCESS("Successfully scraped and saved data"))
