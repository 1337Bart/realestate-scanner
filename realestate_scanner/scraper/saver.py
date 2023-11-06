from scraper.models import RealEstateListing


def save_listing_data(validated_realestate_listing):
    listing = RealEstateListing(
        listing_title=validated_realestate_listing["listing_title"],
        listing_address=validated_realestate_listing["listing_address"],
        price=validated_realestate_listing["price"],
        price_per_sqm=validated_realestate_listing["price_per_sqm"],
        rooms=validated_realestate_listing["rooms"],
        area=validated_realestate_listing["area"],
        url=validated_realestate_listing["url"],
    )

    listing.save()
