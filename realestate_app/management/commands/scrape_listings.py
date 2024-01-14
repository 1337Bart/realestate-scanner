import os
import django
from django.core.management.base import BaseCommand

from realestate_app.models import RealEstateListing
from realestate_app.services.scraper import Scraper
from realestate_app.services.validate import Validator
from realestate_app.services.data_prep import DataPrepare
from realestate_app.services.saver import Saver

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


class Command(BaseCommand):
    help = "Scrape data and store it in the database"

    # todo make sure validation and saving happens every page instead of in bulk after scraping ends
    # todo make sure this can run in parallel
    def handle(self, *args, **options):
        scraper = Scraper()
        saver = Saver()
        raw_data = scraper.scrape_listing_pages(
            building_type="mieszkanie",
            region="slaskie",
            transaction_type="sprzedaz",
            max_pages=7,
        )

        cleaned_listings = DataPrepare.prepare_listing_data(raw_data)
        validated_listings = Validator.validate_listing_data(cleaned_listings)

        if validated_listings:
            saver.save_listings(validated_listings)

        self.stdout.write(self.style.SUCCESS("Successfully scraped and saved data"))
