from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets


router = DefaultRouter()
router.register(r'', viewsets.BookViewSet, basename='book')


urlpatterns = [
    path('', include(router.urls)),
]
