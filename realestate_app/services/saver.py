import logging
from typing import List, Dict, Optional
from models import RealEstateListing

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class Saver:
    @staticmethod
    def save_listings(listings: List[Dict[str, Optional[str]]]):
        for listing in listings:
            Saver.save_listing(listing)
        logging.info("Listings saved successfully.")

    @staticmethod
    def save_listing(validated_realestate_listing: Dict[str, Optional[str]]):
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
        listing.save()
