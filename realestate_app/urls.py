from django.urls import path
from .views import PricePredictionListView
from .views import StartScrapingView
from .views import CalculatePredictionsView


urlpatterns = [
    path(
        "price-predictions/",
        PricePredictionListView.as_view(),
        name="price-predictions",
    ),
    path("start-scraping/", StartScrapingView.as_view(), name="start-scraping"),
    path(
        "calculate-predictions/",
        CalculatePredictionsView.as_view(),
        name="calculate-predictions",
    ),
]
