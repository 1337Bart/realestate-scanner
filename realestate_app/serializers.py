from rest_framework import serializers
from .models import RealEstateListing, PricePrediction


class RealEstateListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = RealEstateListing
        fields = "__all__"


class PricePredictionSerializer(serializers.ModelSerializer):
    listing = RealEstateListingSerializer(read_only=True)
    linear_regression_price_difference = serializers.FloatField(read_only=True)
    multiple_linear_regression_price_difference = serializers.FloatField(read_only=True)
    random_forest_predicted_price_difference = serializers.FloatField(read_only=True)

    class Meta:
        model = PricePrediction
        fields = "__all__"
