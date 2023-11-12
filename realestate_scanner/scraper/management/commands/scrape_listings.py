import os
import django
from django.core.management.base import BaseCommand

from scraper.models import RealEstateListing

from scraper.scraper import scrape_listing_pages
from scraper.validajter import validate_listing_data
from scraper.data_prep import prepare_listing_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "realestate_scanner.settings")
django.setup()


class Command(BaseCommand):
    help = "Scrape data and store it in the database"

    def handle(self, *args, **options):
        scraped_data = scrape_listing_pages(
            building_type="mieszkanie", region="slaskie", transaction_type="sprzedaz"
        )

        for raw_listing in scraped_data:
            cleaned_data = prepare_listing_data(raw_listing)
            validated_data = validate_listing_data(cleaned_data)

            if validated_data:
                listing = RealEstateListing(**validated_data)
                listing.save()

        self.stdout.write(self.style.SUCCESS("Successfully scraped and saved data"))
