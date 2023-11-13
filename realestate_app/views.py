from django.shortcuts import render
from models import RealEstateListing
from rest_framework import viewsets
from .serializers import RealEstateListingSerializer
from models import RealEstateListing


class RealEstateListingViewSet(viewsets.ModelViewSet):
    queryset = RealEstateListing.objects.all()
    serializer_class = RealEstateListingSerializer
