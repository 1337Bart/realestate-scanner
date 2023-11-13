from django.contrib import admin
from models import RealEstateListing

# Register your models here.


@admin.register(RealEstateListing)
class RealEstateListingAdmin(admin.ModelAdmin):
    list_display = ("listing_title", "city", "price", "rooms", "area")
    search_fields = ("listing_title", "city")
