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
