from django.urls import path
from rest_framework.routers import DefaultRouter
from realestate_app.views import RealEstateListingViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r"listings", RealEstateListingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
