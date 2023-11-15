from typing import List, Dict, Optional
from realestate_app.models import RealEstateListing
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Saver:
    @staticmethod
    def save_listings(listings: List[Dict[str, Optional[str]]]):
        real_estate_objects = []

        for validated_realestate_listing in listings:
            listing = RealEstateListing(
                listing_title=validated_realestate_listing["listing_title"],
                price=validated_realestate_listing["price"],
                price_per_sqm=validated_realestate_listing["price_per_sqm"],
                rooms=validated_realestate_listing["rooms"],
                area=validated_realestate_listing["area"],
                url=validated_realestate_listing["url"],
                street=validated_realestate_listing.get("street"),
                district=validated_realestate_listing.get("district"),
                city=validated_realestate_listing.get("city"),
                voivodeship=validated_realestate_listing["voivodeship"],
            )
            real_estate_objects.append(listing)

        RealEstateListing.objects.bulk_create(real_estate_objects)
        logging.info(f"{len(real_estate_objects)} listings saved successfully.")
