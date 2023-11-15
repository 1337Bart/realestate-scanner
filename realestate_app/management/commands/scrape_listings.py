import os
import django
from django.core.management.base import BaseCommand

from realestate_app.models import RealEstateListing
from realestate_app.services.scraper import Scraper
from realestate_app.services.validate import Validator
from realestate_app.services.data_prep import DataPrepare

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


class Command(BaseCommand):
    help = "Scrape data and store it in the database"

    def handle(self, *args, **options):
        scrapITmofo = Scraper()
        scraped_data = scrapITmofo.scrape_listing_pages(
            building_type="mieszkanie", region="slaskie", transaction_type="sprzedaz"
        )

        for raw_listing in scraped_data:
            cleaned_data = DataPrepare.prepare_listing_data(raw_listing)
            validated_data = Validator.validate_listing_data(cleaned_data)

            if validated_data:
                listing = RealEstateListing(**validated_data)
                listing.save()

        self.stdout.write(self.style.SUCCESS("Successfully scraped and saved data"))
