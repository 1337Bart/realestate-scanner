from django.shortcuts import render
from realestate_app.models import RealEstateListing
from rest_framework import viewsets
from .serializers import RealEstateListingSerializer


class RealEstateListingViewSet(viewsets.ModelViewSet):
    queryset = RealEstateListing.objects.all()
    serializer_class = RealEstateListingSerializer
