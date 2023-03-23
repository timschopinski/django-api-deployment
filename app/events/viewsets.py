from .models import Event
from rest_framework import viewsets
from.serializers import EventSerializer


class EventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Book instances.
    """

    serializer_class = EventSerializer
    queryset = Event.objects.all()
