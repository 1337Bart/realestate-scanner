from rest_framework import serializers
from scraper.models import RealEstateListing


class RealEstateListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateListing
        fields = [
            "listing_title",
            "street",
            "district",
            "city",
            "voivodeship",
            "price",
            "price_per_sqm",
            "rooms",
            "area",
            "url",
        ]
