from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import viewsets
from .views import NotificationView


router = DefaultRouter()
router.register(r'', viewsets.EventViewSet, basename='event')


urlpatterns = [
    path('notification/', NotificationView.as_view(), name='notification'),
    path('', include(router.urls)),
]
