from django.db.models import F
from rest_framework import generics
from .models import PricePrediction
from .serializers import PricePredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services.scraper import Scraper
from .services.validate import Validator
from .services.data_prep import DataPrepare
from .services.saver import Saver
from .services.price_prediction import calculate_predictions


class PricePredictionListView(generics.ListAPIView):
    serializer_class = PricePredictionSerializer

    def get_queryset(self):
        queryset = (
            PricePrediction.objects.select_related("listing")
            .annotate(
                linear_regression_price_difference=F("listing__price")
                - F("simple_linear_regression_predicted_price")
            )
            .annotate(
                multiple_linear_regression_price_difference=F("listing__price")
                - F("multiple_linear_regression_predicted_price")
            )
            .annotate(
                random_forest_predicted_price_difference=F("listing__price")
                - F("random_forest_predicted_price")
            )
        )
        city = self.request.query_params.get("city", None)
        voivodeship = self.request.query_params.get("voivodeship", None)
        district = self.request.query_params.get("district", None)
        ordering = self.request.query_params.get("ordering", None)

        # TODO: dodac filtrowanie diacritic i case insesitive
        if city:
            queryset = queryset.filter(listing__city=city)
        if voivodeship:
            queryset = queryset.filter(listing__voivodeship=voivodeship)
        if district:
            queryset = queryset.filter(listing__district=district)
        if ordering:
            queryset = queryset.order_by(ordering)

        return queryset


class StartScrapingView(APIView):
    def post(self, request, format=None):
        building_type = request.data.get("building_type", "mieszkanie")
        region = request.data.get("region", "slaskie")
        transaction_type = request.data.get("transaction_type", "sprzedaz")
        max_pages = request.data.get("max_pages", 1)

        scraper = Scraper()
        saver = Saver()
        raw_data = scraper.scrape_listing_pages(
            building_type=building_type,
            region=region,
            transaction_type=transaction_type,
            max_pages=max_pages,
        )

        cleaned_listings = DataPrepare.prepare_listing_data(raw_data)
        validated_listings = Validator.validate_listing_data(cleaned_listings)

        if validated_listings:
            saver.save_listings(validated_listings)

        return Response({"status": "Scraping initiated"}, status=status.HTTP_200_OK)


class CalculatePredictionsView(APIView):
    def get(self, request, format=None):
        calculate_predictions()
        return Response(
            {"status": "Predictions calculation started"}, status=status.HTTP_200_OK
        )
