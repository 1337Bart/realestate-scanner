from django.db import models


class RealEstateListing(models.Model):
    listing_title = models.CharField(max_length=255)
    street = models.CharField(max_length=255, null=True, blank=True)
    district = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    voivodeship = models.CharField(max_length=255)
    price = models.IntegerField()
    price_per_sqm = models.FloatField()
    rooms = models.IntegerField()
    area = models.FloatField()
    url = models.URLField()

    def __str__(self):
        return f"{self.listing_title} - {self.price} zł"


class PricePrediction(models.Model):
    listing = models.OneToOneField(RealEstateListing, on_delete=models.CASCADE)
    simple_linear_regression_predicted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    multiple_linear_regression_predicted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    random_forest_predicted_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    prediction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.method} prediction for {self.listing.listing_title}"
