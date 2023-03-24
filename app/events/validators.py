from rest_framework import serializers
from events.models import Event
from django.core.exceptions import ObjectDoesNotExist


class EventExistsValidator:

    def __call__(self, event_id: int):
        try:
            Event.objects.get(id=event_id)
        except ObjectDoesNotExist:
            message = f'Invalid Event ID: {event_id}'
            raise serializers.ValidationError(message)
