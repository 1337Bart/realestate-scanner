import os
import django
from django.core.management.base import BaseCommand

from realestate_app.services.price_prediction import (
    calculate_predictions,
)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


class Command(BaseCommand):
    help = "Calculate price predictions and store them in database"

    def handle(self, *args, **options):
        calculate_predictions()

        self.stdout.write(self.style.SUCCESS("Successfully calculated predictions"))
